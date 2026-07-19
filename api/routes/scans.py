"""
Scans router.
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.dependencies import get_current_active_user
from api.models.scan import Scan
from api.models.finding import Finding
from api.models.dimension_score import DimensionScoreModel
from api.models.session import get_db
from api.models.user import User
from api.schemas.scan import ScanRequest, ScanResponse, ScanDetailResponse, FindingResponse, DimensionScoreResponse
from api.services.scan_service import create_and_queue_scan

router = APIRouter()


@router.post("/", response_model=ScanResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_scan(
    scan_in: ScanRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> ScanResponse:
    """Queues a new security scan."""
    scan = await create_and_queue_scan(db, scan_in, current_user)
    return scan


@router.get("/", response_model=list[ScanResponse])
async def list_scans(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> list[ScanResponse]:
    """Lists previous scans for the authenticated user."""
    result = await db.execute(
        select(Scan)
        .where(Scan.user_id == current_user.id)
        .order_by(Scan.created_at.desc())
    )
    return list(result.scalars().all())


@router.get("/{scan_id}", response_model=ScanResponse)
async def get_scan_status(
    scan_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> ScanResponse:
    """Gets the status and details of a specific scan."""
    result = await db.execute(
        select(Scan).where(Scan.id == scan_id).where(Scan.user_id == current_user.id)
    )
    scan = result.scalar_one_or_none()

    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    return scan


@router.get("/{scan_id}/detail", response_model=ScanDetailResponse)
async def get_scan_detail(
    scan_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> ScanDetailResponse:
    """Gets full scan details including findings and dimension scores."""
    result = await db.execute(
        select(Scan)
        .where(Scan.id == scan_id)
        .where(Scan.user_id == current_user.id)
        .options(
            selectinload(Scan.findings),
            selectinload(Scan.dimension_scores),
        )
    )
    scan = result.scalar_one_or_none()

    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    return ScanDetailResponse(
        id=scan.id,
        target_url=scan.target_url,
        status=scan.status,
        profile=scan.profile,
        overall_score=scan.overall_score,
        overall_grade=scan.overall_grade,
        created_at=scan.created_at,
        completed_at=scan.completed_at,
        findings=[
            FindingResponse(
                id=f.id,
                owasp_id=f.owasp_id,
                owasp_name=f.owasp_name,
                dimension=f.dimension,
                passed=f.passed,
                severity=f.severity,
                title=f.title,
                description=f.description,
                business_impact=f.business_impact,
                recommendation=f.recommendation,
                effort=f.effort,
                evidence=f.evidence,
                references=f.references,
            )
            for f in scan.findings
        ],
        dimension_scores=[
            DimensionScoreResponse(
                id=d.id,
                dimension=d.dimension,
                score=d.score,
                weight=d.weight,
                grade=d.grade,
                label=d.label,
            )
            for d in scan.dimension_scores
        ],
    )

