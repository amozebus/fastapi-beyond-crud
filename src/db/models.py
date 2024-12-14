"""Database models"""

from dataclasses import dataclass

import uuid

import sqlalchemy.dialects.postgresql as pg

from sqlmodel import Column, Field, SQLModel


@dataclass
class User(SQLModel, table=True):
    """Database User model"""

    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4, unique=True
        )
    )
    username: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, unique=True))
    password_hash: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False), exclude=True
    )
