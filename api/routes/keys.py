"""
API Keys router.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_active_user
from api.models.api_key import ApiKey
from api.models.session import get_db
from api.models.user import User
from api.schemas.auth import ApiKeyCreate, ApiKeyListResponse, ApiKeyResponse
from api.services.auth_service import generate_api_key_and_hash

router = APIRouter()


@router.post("/", response_model=ApiKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    key_in: ApiKeyCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> ApiKeyResponse:
    """Creates a new API key for the authenticated user."""
    raw_key, key_hash = generate_api_key_and_hash()

    api_key = ApiKey(name=key_in.name, key_hash=key_hash, user_id=current_user.id)
    db.add(api_key)
    await db.commit()
    await db.refresh(api_key)

    # Return the raw key ONLY once. It's not stored.
    response = ApiKeyResponse(id=api_key.id, name=api_key.name, key=raw_key)
    return response


@router.get("/", response_model=list[ApiKeyListResponse])
async def list_api_keys(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> list[ApiKeyListResponse]:
    """Lists all API keys for the authenticated user."""
    result = await db.execute(select(ApiKey).where(ApiKey.user_id == current_user.id))
    keys = result.scalars().all()

    return [
        ApiKeyListResponse(
            id=k.id,
            name=k.name,
            last_used_at=k.last_used_at.isoformat() if k.last_used_at else None,
        )
        for k in keys
    ]


@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_api_key(
    key_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Revokes an API key."""
    result = await db.execute(
        select(ApiKey)
        .where(ApiKey.id == key_id)
        .where(ApiKey.user_id == current_user.id)
    )
    api_key = result.scalar_one_or_none()

    if not api_key:
        raise HTTPException(status_code=404, detail="API Key not found")

    await db.delete(api_key)
    await db.commit()
