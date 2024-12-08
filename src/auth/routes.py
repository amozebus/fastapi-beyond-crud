"""API Authentication requests handlers"""

from fastapi import APIRouter, Depends

from sqlmodel.ext.asyncio.session import AsyncSession

from db import get_db_session
from db.models import User

from .models import Token
from .schemas import UserCreate, UserLogin
from .utils import create_token, block_jti
from .service import create_user, auth_user, get_user
from .dependencies import RefreshTokenBearer

r = APIRouter(prefix="/auth")


@r.post("/register", response_model=User)
async def register(
    user_data: UserCreate, db_session: AsyncSession = Depends(get_db_session)
) -> User:
    """Register user"""
    return await create_user(user_data, db_session)


@r.post("/login", response_model=list[Token])
async def login(
    user_data: UserLogin, db_session: AsyncSession = Depends(get_db_session)
) -> list[Token]:
    """Get access and refresh tokens"""
    user = await auth_user(user_data, db_session)

    return [
        Token(token=create_token(user)),
        Token(token=create_token(user, refresh=True), refresh=True),
    ]


@r.post("/refresh", response_model=list[Token])
async def refresh(
    token_data: dict = Depends(RefreshTokenBearer()),
    db_session: AsyncSession = Depends(get_db_session),
) -> list[Token]:
    """Refresh tokens"""
    await block_jti(token_data["jti"])

    user = await get_user(token_data["username"], db_session)

    return [
        Token(token=create_token(user)),
        Token(token=create_token(user, refresh=True), refresh=True),
    ]
