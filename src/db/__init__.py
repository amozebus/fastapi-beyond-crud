"""Database initialization"""
from typing import AsyncGenerator

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import settings

db_url = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_USER_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

async_engine: AsyncEngine = create_async_engine(
    db_url,
    future=True
)

async def init_database() -> None:
    """Initializate and start database engine"""
    async with async_engine.begin() as async_conn:
        await async_conn.run_sync(SQLModel.metadata.create_all)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session"""
    async_session_maker = sessionmaker(
        bind=async_engine, 
        class_=AsyncSession, 
        autoflush=False,
        expire_on_commit=False
    )
    async with async_session_maker() as db_session:
        yield db_session
