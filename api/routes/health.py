"""
Healthcheck router.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check() -> dict[str, str]:
    """Returns the API health status."""
    return {"status": "ok", "service": "webguard-api"}
