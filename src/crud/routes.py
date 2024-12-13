"""CRUD template"""

from typing import Any, Annotated

from fastapi import APIRouter, Depends, Request

from db.models import User

from auth.dependencies import get_current_user

from rate_limit import rate_limit

r = APIRouter(prefix="/crud")


@r.get("/unprotected", response_model=dict[str, str])
@rate_limit(max_calls=5, period=60)
async def hello_world(request: Request) -> dict[str, str]:
    """Unprotected handler template"""

    return {"message": "Hello, world!"}


@r.get("/protected", response_model=dict[str, Any])
@rate_limit(max_calls=5, period=60)
async def hello_world_protected(
    request: Request, user: Annotated[User, Depends(get_current_user)]
) -> dict[str, Any]:
    """Protected handler template"""

    return {"message": "Hello, world!", "user": user}
