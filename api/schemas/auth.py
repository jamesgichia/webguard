"""
Auth and User schemas.
"""

import uuid
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True


class ApiKeyCreate(BaseModel):
    name: str


class ApiKeyResponse(BaseModel):
    id: uuid.UUID
    name: str
    key: str  # Plain text key (only returned once)

    class Config:
        from_attributes = True


class ApiKeyListResponse(BaseModel):
    id: uuid.UUID
    name: str
    last_used_at: str | None = None

    class Config:
        from_attributes = True
