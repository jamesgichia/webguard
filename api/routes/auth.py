"""
Auth router.
"""

import os
import uuid
import emails
from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt

from api.models.session import get_db
from api.models.user import User
from api.schemas.auth import Token, UserCreate, UserResponse
from api.services.auth_service import (
    create_access_token,
    get_password_hash,
    verify_password,
    SECRET_KEY,
    ALGORITHM,
)
from api.dependencies import limiter

router = APIRouter()

def send_verification_email(email: str, token: str):
    # Sends a verification email (only if SMTP is configured)
    if os.getenv("EMAIL_VERIFICATION_ENABLED", "false").lower() == "true":
        message = emails.html(
            html=f"<p>Please verify your WebGuard account by clicking the link: <a href='http://localhost:5173/verify?token={token}'>Verify Email</a></p>",
            subject="Verify your WebGuard account",
            mail_from=os.getenv("SMTP_FROM", "noreply@webguard.local")
        )
        message.send(
            smtp={
                "host": os.getenv("SMTP_HOST", "localhost"),
                "port": int(os.getenv("SMTP_PORT", 587)),
                "user": os.getenv("SMTP_USER", ""),
                "password": os.getenv("SMTP_PASSWORD", ""),
                "tls": True
            }
        )

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(request: Request, user_in: UserCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)) -> UserResponse:
    """Registers a new user."""
    existing_user = await db.scalar(select(User).where(User.email == user_in.email))
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        is_active=True,
        is_verified=False,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    verification_token = create_access_token(data={"sub": user.email, "type": "verify"})
    background_tasks.add_task(send_verification_email, user.email, verification_token)

    return user

@router.get("/verify")
@limiter.limit("10/minute")
async def verify_email(request: Request, token: str, db: AsyncSession = Depends(get_db)):
    """Verifies a user's email address."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        token_type = payload.get("type")
        if email is None or token_type != "verify":
            raise HTTPException(status_code=400, detail="Invalid token")
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = await db.scalar(select(User).where(User.email == email))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.is_verified:
        return {"msg": "Email already verified"}

    user.is_verified = True
    await db.commit()
    return {"msg": "Email verified successfully"}

@router.post("/token", response_model=Token)
@limiter.limit("10/minute")
async def login_for_access_token(
    request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
) -> Token:
    """Authenticates a user and returns a JWT token."""
    user = await db.scalar(select(User).where(User.email == form_data.username))
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_verified and os.getenv("EMAIL_VERIFICATION_ENABLED", "false").lower() == "true":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please check your inbox.",
        )

    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")
