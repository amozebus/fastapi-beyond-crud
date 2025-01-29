"""Service for requests handlers"""

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.models import User

from .utils import hash_password, verify_password
from .schemas import UserCreate


async def get_user(username: str, db_session: AsyncSession) -> User:
    """Get user from database by username"""
    statement = select(User).where(User.username == username)
    result = await db_session.exec(statement)
    await db_session.close()

    return result.first()


async def create_user(user_data: UserCreate, db_session: AsyncSession) -> User:
    """Add user to database"""
    if await get_user(user_data.username, db_session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is unavailable",
        )

    user = User(**user_data.model_dump())
    user.password_hash = hash_password(user_data.password)

    db_session.add(user)
    await db_session.commit()
    await db_session.close()

    return user


async def auth_user(
    user_data: OAuth2PasswordRequestForm, db_session: AsyncSession
) -> User:
    """Authenticate user"""
    user = await get_user(user_data.username, db_session)
    if user:
        if verify_password(user_data.password, user.password_hash):
            return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
    )
