"""
Dashboard stats router.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_active_user
from api.models.scan import Scan
from api.models.session import get_db
from api.models.user import User

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Gets aggregate statistics for the user's dashboard."""
    # Count total scans
    total_result = await db.execute(
        select(func.count(Scan.id)).where(Scan.user_id == current_user.id)
    )
    total_scans = total_result.scalar() or 0

    # Average score
    avg_result = await db.execute(
        select(func.avg(Scan.overall_score))
        .where(Scan.user_id == current_user.id)
        .where(Scan.status == "completed")
    )
    avg_score = avg_result.scalar() or 0.0

    return {
        "total_scans": total_scans,
        "average_score": round(avg_score, 1),
    }
