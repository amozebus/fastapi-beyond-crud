"""Authentication dependencies for requests handlers"""

from typing import Annotated, Union

from sqlalchemy.ext.asyncio.session import AsyncSession

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.param_functions import Form

from db import get_db_session
from db.models import User

from .utils import decode_token, jti_blocked
from .service import get_user
from .exceptions import BearerTokenException


class OAuth2RefreshRequestForm(OAuth2PasswordRequestForm):
    """
    Like `fastapi.security.oauth2.OAuth2PasswordRequest`
    for tokens refresh request
    """

    def __init__(
        self,
        grant_type: Annotated[Union[str, None], Form(pattern="refresh_token")],
        refresh_token: Annotated[str, Form()],
    ):
        self.grant_type = grant_type
        self.refresh_token = refresh_token


bearer = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


async def get_current_user(
    token: Annotated[str, Depends(bearer)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> User:
    """
    Get current user via access token data.
    Use as dependency to authorize user
    """
    token_data = decode_token(token)
    if token_data["refresh"]:
        raise BearerTokenException(detail="Provide access token")

    if await jti_blocked(token_data["jti"]):
        raise BearerTokenException(detail="Revoked token")

    user = await get_user(token_data["username"], db_session)

    return user
