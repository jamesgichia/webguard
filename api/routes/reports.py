"""
Reports router.
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_active_user
from api.models.report import Report
from api.models.scan import Scan
from api.models.session import get_db
from api.models.user import User
from api.schemas.report import ReportResponse

router = APIRouter()


@router.get("/{scan_id}", response_model=ReportResponse)
async def get_report_metadata(
    scan_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> ReportResponse:
    """Gets metadata about available reports for a scan."""
    result = await db.execute(
        select(Scan).where(Scan.id == scan_id).where(Scan.user_id == current_user.id)
    )
    scan = result.scalar_one_or_none()

    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    result = await db.execute(select(Report).where(Report.scan_id == scan_id))
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(status_code=404, detail="Report not ready yet")

    return ReportResponse(
        id=report.id,
        scan_id=report.scan_id,
        has_html=False,  # Can be implemented by generating on the fly
        has_pdf=False,
    )


@router.get("/{scan_id}/download/json")
async def download_json_report(
    scan_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Downloads the raw JSON report for a scan."""
    result = await db.execute(
        select(Scan).where(Scan.id == scan_id).where(Scan.user_id == current_user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Scan not found")

    result = await db.execute(select(Report).where(Report.scan_id == scan_id))
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(status_code=404, detail="Report not ready yet")

    return report.json_data
