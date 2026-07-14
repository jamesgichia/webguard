"""
Database session management.
"""

import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://webguard:webguard@localhost:5432/webguard")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for providing a database session."""
    async with AsyncSessionLocal() as session:
        yield session
