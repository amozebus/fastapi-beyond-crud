"""Schemas for requests bodies"""

from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class UserCreate(BaseModel):
    """Registration schema"""

    username: str
    password: str
