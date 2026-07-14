"""
Scan service.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from api.models.scan import Scan
from api.models.user import User
from api.schemas.scan import ScanRequest
from api.workers.scan_tasks import run_scan_job


async def create_and_queue_scan(
    db: AsyncSession, scan_in: ScanRequest, user: User
) -> Scan:
    """Creates a scan record and queues the Celery task."""
    scan = Scan(
        target_url=scan_in.target_url,
        profile=scan_in.profile,
        user_id=user.id,
        status="pending",
    )
    db.add(scan)
    await db.commit()
    await db.refresh(scan)

    # Trigger Celery task asynchronously
    run_scan_job.delay(str(scan.id), scan.target_url)

    return scan
