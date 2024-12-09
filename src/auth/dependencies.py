"""Authentication dependencies for requests handlers"""

from typing import Annotated

from sqlalchemy.ext.asyncio.session import AsyncSession

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from db import get_db_session
from db.models import User

from .utils import decode_token, jti_blocked
from .service import get_user

bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: Annotated[str, Depends(bearer)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> User:
    token_data = decode_token(token)
    if await jti_blocked(token_data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Revoked token"
        )

    user = await get_user(token_data['username'], db_session)

    return user