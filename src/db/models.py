"""Database models"""

from dataclasses import dataclass

import sqlalchemy.dialects.postgresql as pg

from sqlmodel import Column, Field, SQLModel


@dataclass
class User(SQLModel, table=True):
    """Database User model"""

    __tablename__ = "users"

    id: int = Field(
        sa_column=Column(
            pg.INTEGER, nullable=False, primary_key=True, unique=True
        )
    )
    username: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, unique=True))
    password_hash: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False), exclude=True
    )
