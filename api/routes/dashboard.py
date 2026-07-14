"""
Dashboard stats router.
"""

from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_current_active_user
from api.models.user import User

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """Gets aggregate statistics for the user's dashboard."""
    raise HTTPException(status_code=501, detail="Not implemented yet")
