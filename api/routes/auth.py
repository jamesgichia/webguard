"""
Auth router.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.schemas.auth import Token, UserCreate, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate) -> UserResponse:
    """Registers a new user."""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """Authenticates a user and returns a JWT token."""
    raise HTTPException(status_code=501, detail="Not implemented yet")
