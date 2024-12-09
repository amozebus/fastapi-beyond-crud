"""CRUD template"""
from typing import Any, Annotated

from fastapi import APIRouter, Depends

from db.models import User

from auth.dependencies import get_current_user

r = APIRouter(prefix="/crud")


@r.get("/unprotected", response_model=dict[str, str])
async def hello_world() -> dict[str, str]:
    """Unprotected handler template"""
    return {"message": "Hello, world!"}


@r.get("/protected", response_model=dict[str, Any])
async def hello_world_protected(
    user: Annotated[User, Depends(get_current_user)]
) -> dict[str, Any]:
    """Protected handler template"""
    return {"message": "Hello, world!", "user": user}
