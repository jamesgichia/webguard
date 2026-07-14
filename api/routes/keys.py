"""
API Keys router.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import get_current_active_user
from api.models.user import User
from api.schemas.auth import ApiKeyCreate, ApiKeyListResponse, ApiKeyResponse

router = APIRouter()


@router.post("/", response_model=ApiKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    key_in: ApiKeyCreate, current_user: User = Depends(get_current_active_user)
) -> ApiKeyResponse:
    """Creates a new API key for the authenticated user."""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/", response_model=list[ApiKeyListResponse])
async def list_api_keys(
    current_user: User = Depends(get_current_active_user)
) -> list[ApiKeyListResponse]:
    """Lists all API keys for the authenticated user."""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_api_key(
    key_id: str, current_user: User = Depends(get_current_active_user)
) -> None:
    """Revokes an API key."""
    raise HTTPException(status_code=501, detail="Not implemented yet")
