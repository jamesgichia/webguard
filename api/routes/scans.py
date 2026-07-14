"""
Scans router.
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import get_current_active_user
from api.models.user import User
from api.schemas.scan import ScanRequest, ScanResponse

router = APIRouter()


@router.post("/", response_model=ScanResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_scan(
    scan_in: ScanRequest, current_user: User = Depends(get_current_active_user)
) -> ScanResponse:
    """Queues a new security scan."""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/", response_model=list[ScanResponse])
async def list_scans(
    current_user: User = Depends(get_current_active_user)
) -> list[ScanResponse]:
    """Lists previous scans for the authenticated user."""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{scan_id}", response_model=ScanResponse)
async def get_scan_status(
    scan_id: uuid.UUID, current_user: User = Depends(get_current_active_user)
) -> ScanResponse:
    """Gets the status and details of a specific scan."""
    raise HTTPException(status_code=501, detail="Not implemented yet")
