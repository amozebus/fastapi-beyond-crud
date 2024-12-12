"""API Authentication requests handlers"""

from typing import Annotated

from fastapi import APIRouter, Request, Response, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlmodel.ext.asyncio.session import AsyncSession

from db import get_db_session
from db.models import User

from .models import Token
from .schemas import UserCreate
from .utils import create_token, decode_token, block_jti, jti_blocked
from .service import create_user, auth_user
from .dependencies import bearer

r = APIRouter(prefix="/auth")


@r.post("/register", response_model=User)
async def register(
    user_data: UserCreate,
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> User:
    """Register user"""
    return await create_user(user_data, db_session)


@r.post("/login", response_model=Token)
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: AsyncSession = Depends(get_db_session)
) -> Token:
    """Get access and refresh tokens"""
    user = await auth_user(form_data, db_session)

    response.set_cookie(
        key="refresh_token",
        value=create_token(user, refresh=True),
        httponly=True,
        secure=True
    )

    return Token(
        access_token=create_token(user),
        token_type="bearer"
    )

@r.post("/refresh", response_model=Token)
async def refresh(
    request: Request,
    response: Response
) -> Token:
    """Refresh tokens"""
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing"
        )

    refresh_token_data = decode_token(refresh_token)
    if await jti_blocked(refresh_token_data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Revoked token"
        )

    user = User(**refresh_token_data)
    user.uid = refresh_token_data["sub"]

    await block_jti(refresh_token_data["jti"], refresh=True)
    
    response.set_cookie(
        key="refresh_token",
        value=create_token(user, refresh=True),
        httponly=True,
        secure=True
    )

    return Token(
        access_token=create_token(user),
        token_type="bearer"
    )

@r.post("/logout", response_model=dict[str, str])
async def logout(
    request: Request,
    response: Response,
    access_token: Annotated[str, Depends(bearer)]
) -> dict[str, str]:
    refresh_token = request.cookies.get("refresh_token")
    refresh_token_data = decode_token(refresh_token)

    access_token_data = decode_token(access_token)

    await block_jti(access_token_data["jti"])
    await block_jti(refresh_token_data["jti"], refresh=True)
    
    response.delete_cookie(key="refresh_token")

    return {
        "message": "Logged out successfully"
    }