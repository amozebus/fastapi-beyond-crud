"""Authentication dependencies for requests handlers"""
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .utils import decode_token, jti_blocked

class TokenBearer(HTTPBearer):
    """Base bearer class"""
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | dict | None:
        """Decode and verify encoded JWT"""
        creds = await super().__call__(request)

        encoded_jwt = creds.credentials

        token_data = decode_token(encoded_jwt=encoded_jwt)

        if token_data:
            if await jti_blocked(token_data["jti"]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Revoked token"
                )

            self.bearer(token_data)

            return token_data

    def bearer(self, token_data: dict):
        raise NotImplementedError()

class AccessTokenBearer(TokenBearer):
    """Bearer for access tokens"""
    def bearer(self, token_data: dict):
        if token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Provide access token"
            )

class RefreshTokenBearer(TokenBearer):
    """Bearer for refresh tokens"""
    def bearer(self, token_data: dict):
        if not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Provide refresh token"
            )