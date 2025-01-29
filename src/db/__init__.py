"""Database initialization"""

from typing import AsyncGenerator

from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import settings

async_engine: AsyncEngine = create_async_engine(settings.DATABASE_URL, future=True)

async_session_maker = sessionmaker(
    bind=async_engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session"""
    
    yield async_session_maker()
