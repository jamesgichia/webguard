"""
Reports router.
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_current_active_user
from api.models.user import User
from api.schemas.report import ReportResponse

router = APIRouter()


@router.get("/{scan_id}", response_model=ReportResponse)
async def get_report_metadata(
    scan_id: uuid.UUID, current_user: User = Depends(get_current_active_user)
) -> ReportResponse:
    """Gets metadata about available reports for a scan."""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{scan_id}/download/json")
async def download_json_report(
    scan_id: uuid.UUID, current_user: User = Depends(get_current_active_user)
) -> dict:
    """Downloads the raw JSON report for a scan."""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{scan_id}/download/html")
async def download_html_report(
    scan_id: uuid.UUID, current_user: User = Depends(get_current_active_user)
) -> str:
    """Downloads the HTML report for a scan."""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{scan_id}/download/pdf")
async def download_pdf_report(
    scan_id: uuid.UUID, current_user: User = Depends(get_current_active_user)
) -> bytes:
    """Downloads the PDF report for a scan."""
    raise HTTPException(status_code=501, detail="Not implemented yet")
