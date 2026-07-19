"""
Celery worker for executing security scans.
"""

import asyncio
import json
import os
from datetime import datetime, timezone

from celery import Celery
from sqlalchemy import select, update

from api.models.dimension_score import DimensionScoreModel
from api.models.finding import Finding
from api.models.report import Report as ReportModel
from api.models.scan import Scan
from api.models.session import AsyncSessionLocal
from engine.fetcher import fetch_target
from engine.models import ScanReport
from engine.orchestrator import ScanOrchestrator
from engine.reporter import Reporter
from engine.scorer import Scorer

celery_app = Celery(
    "webguard",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1"),
)

celery_app.conf.update(
    task_always_eager=os.getenv("CELERY_TASK_ALWAYS_EAGER", "True").lower() == "true",
    task_eager_propagates=True,
)


import asyncio

@celery_app.task(name="scan_tasks.run_scan_job")
def run_scan_job(scan_id: str, target_url: str) -> None:
    """Entry point for the celery task."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # Running synchronously within FastAPI (CELERY_TASK_ALWAYS_EAGER=True)
        loop.create_task(_async_run_scan_job(scan_id, target_url))
    else:
        # Running in a standard Celery worker
        asyncio.run(_async_run_scan_job(scan_id, target_url))


async def _async_run_scan_job(scan_id: str, target_url: str) -> None:
    """Async implementation of the scan job."""
    try:
        # Update status to running
        async with AsyncSessionLocal() as db:
            await db.execute(update(Scan).where(Scan.id == scan_id).values(status="running"))
            await db.commit()

        target = await fetch_target(target_url)
        orchestrator = ScanOrchestrator()
        results = orchestrator.run_all(target)

        scorer = Scorer()
        score = scorer.calculate(results)

        # Save to database
        async with AsyncSessionLocal() as db:
            scan = await db.scalar(select(Scan).where(Scan.id == scan_id))
            if not scan:
                return

            scan.status = "completed"
            scan.overall_score = score.overall_score
            scan.overall_grade = score.overall_grade
            scan.completed_at = datetime.now(timezone.utc)

            for res in results:
                f = Finding(
                    scan_id=scan.id,
                    owasp_id=res.owasp_id,
                    owasp_name=res.owasp_name,
                    dimension=res.dimension,
                    passed=res.passed,
                    severity=res.severity,
                    title=res.title,
                    description=res.description,
                    business_impact=res.business_impact,
                    recommendation=res.recommendation,
                    effort=res.effort,
                    evidence=res.evidence,
                    references=res.references,
                )
                db.add(f)

            for dim in score.dimensions:
                d = DimensionScoreModel(
                    scan_id=scan.id,
                    dimension=dim.dimension,
                    score=dim.score,
                    weight=dim.weight,
                    grade=dim.grade,
                    label=dim.label,
                )
                db.add(d)

            report_data = ScanReport(
                target_url=target.url,
                scan_time_utc=scan.completed_at.isoformat(),
                score=score,
                results=results,
            )
            reporter = Reporter()
            json_report = reporter.generate_json(report_data)

            rm = ReportModel(scan_id=scan.id, json_data=json.loads(json_report))
            db.add(rm)

            await db.commit()

    except Exception as e:
        async with AsyncSessionLocal() as db:
            await db.execute(update(Scan).where(Scan.id == scan_id).values(status="failed"))
            await db.commit()
        raise e
