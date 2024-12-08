"""Schemas for requests bodies"""

from pydantic import BaseModel


class UserCreate(BaseModel):
    """Registration schema"""

    username: str
    password: str


class UserLogin(UserCreate):
    """Login schema"""

    pass
