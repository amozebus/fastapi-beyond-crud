"""API Authentication requests handlers"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlmodel.ext.asyncio.session import AsyncSession

from db import get_db_session
from db.models import User

from .models import Token
from .schemas import UserCreate
from .utils import create_token, decode_token, block_jti, jti_blocked
from .service import create_user, auth_user
from .dependencies import OAuth2RefreshRequestForm
from .exceptions import BearerTokenException

r = APIRouter(prefix="/auth")


@r.post("/register", response_model=User)
async def register(
    user_data: UserCreate, db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> User:
    """Register user"""
    return await create_user(user_data, db_session)


@r.post("/token", response_model=Token)
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: AsyncSession = Depends(get_db_session),
) -> Token:
    """Get access and refresh tokens"""

    user = await auth_user(form_data, db_session)

    return Token(
        access_token=create_token(user), refresh_token=create_token(user, refresh=True)
    )


@r.post("/token/refresh", response_model=Token)
async def refresh(form_data: Annotated[OAuth2RefreshRequestForm, Depends()]) -> Token:
    refresh_token = form_data.refresh_token
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing"
        )

    refresh_token_data = decode_token(refresh_token)
    if not refresh_token_data["refresh"]:
        raise BearerTokenException(detail="Provide refresh token")
    if await jti_blocked(refresh_token_data["jti"]):
        raise BearerTokenException(detail="Revoked token")

    user = User(**refresh_token_data)
    user.uid = refresh_token_data["sub"]

    await block_jti(refresh_token_data["jti"], refresh=True)

    return Token(
        access_token=create_token(user), refresh_token=create_token(user, refresh=True)
    )
