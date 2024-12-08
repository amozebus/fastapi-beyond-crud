"""CRUD template"""

from fastapi import APIRouter, Depends

from auth.dependencies import AccessTokenBearer

r = APIRouter(prefix="/crud")


@r.get("/unprotected", response_model=dict)
async def hello_world() -> dict:
    """Unprotected handler template"""
    return {"message": "Hello, world!"}


@r.get("/protected", response_model=dict)
async def hello_world_protected(
    token_data: dict = Depends(AccessTokenBearer()),
) -> dict:
    """Protected handler template"""
    return {"message": "Hello, world!", "token_data": token_data}
