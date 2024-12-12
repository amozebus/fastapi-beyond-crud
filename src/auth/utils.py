"""Utils for passwords and tokens"""

import uuid
import time

from datetime import datetime, timedelta, timezone

import jwt

from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from passlib.context import CryptContext

from fastapi import HTTPException, status

from db.models import User
from db.jti_blocklist import jti_blocklist

from config import settings

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Get password hash"""
    return pwd_ctx.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify plain password"""
    return pwd_ctx.verify(password, password_hash)


def create_token(user: User, refresh: bool = False) -> str:
    """Get encoded JWT"""
    exp_delta = (
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE)
        if refresh
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
    )

    return jwt.encode(
        headers={"alg": "HS256", "typ": "JWT"},
        payload={
            "sub": str(user.uid),
            "username": user.username,
            "iat": int(time.time()),
            "exp": datetime.now(timezone.utc) + exp_delta,
            "refresh": refresh,
            "jti": str(uuid.uuid4()),
        },
        key=settings.JWT_SECRET_KEY,
    )


def decode_token(encoded_jwt: str) -> dict:
    """Get decoded token data"""
    try:
        token_data = jwt.decode(
            jwt=encoded_jwt, key=settings.JWT_SECRET_KEY, algorithms=["HS256"]
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return token_data


async def block_jti(jti: str, refresh: bool = False) -> None:
    expiry = settings.REFRESH_TOKEN_EXPIRE * 24 * 60 * 60 if refresh else settings.ACCESS_TOKEN_EXPIRE * 60
    """Add to blocklist (revoke) token with provided JTI"""
    await jti_blocklist.set(name=jti, value="", ex=expiry)


async def jti_blocked(jti: str) -> bool:
    """Check is JTI in blocklist"""
    return True if await jti_blocklist.get(name=jti) is not None else False
