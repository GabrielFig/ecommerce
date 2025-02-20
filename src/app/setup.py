import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.core.config import get_settings
from app.routers import users
from app.services.events import on_shutdown, on_startup
from app.services.handlers import (
    http_exception_handler,
    request_validation_exception_handler,
    unhandled_exception_handler,
)


def setup_routers(app: FastAPI) -> None:
    app.include_router(users.router, prefix=get_settings().api_prefix)

@asynccontextmanager
async def setup_lifespan(app: FastAPI) -> None:
    await on_startup()
    yield
    await on_shutdown()


def setup_logger() -> None:
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.disabled = True


def setup_handlers(app: FastAPI) -> None:
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(
        RequestValidationError, request_validation_exception_handler
    )
    app.add_exception_handler(Exception, unhandled_exception_handler)


def create_app() -> FastAPI:
    setup_logger()

    app = FastAPI(lifespan=setup_lifespan)

    setup_handlers(app)
    setup_routers(app)

    return app
