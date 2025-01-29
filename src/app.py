"""App initialization"""

import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI

from auth.routes import r as auth_router
from crud.routes import r as crud_router

@asynccontextmanager
async def lifespan(application: FastAPI):
    """On-startup and on-shutdown events"""
    logging.info("%s startup", application.title)
    yield
    logging.info("%s shutdown", application.title)


app = FastAPI(title="Beyond CRUD", version="v1", lifespan=lifespan, root_path="/api/")

app.include_router(auth_router)
app.include_router(crud_router)
