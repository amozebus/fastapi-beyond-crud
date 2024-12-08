"""Response models for requests handlers"""

from pydantic import BaseModel


class Token(BaseModel):
    token: str
    refresh: bool = False
