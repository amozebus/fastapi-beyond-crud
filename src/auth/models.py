"""Response models"""

from dataclasses import dataclass

from pydantic import BaseModel

from config import settings


@dataclass
class Token(BaseModel):
    """Token response model"""

    access_token: str
    refresh_token: str
    expires_in: int = settings.ACCESS_TOKEN_EXPIRE * 60
    token_type: str = "Bearer"
