"""
Database session management.
"""

import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"))

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./webguard.db")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db() -> None:
    """Initialize database tables."""
    from api.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for providing a database session."""
    async with AsyncSessionLocal() as session:
        yield session
