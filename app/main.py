
import logging
from fastapi import FastAPI
from app.routers import users
from app.api.v1.endpoints import users, mongo_users
from app.core.database import init_db
from app.core.config import get_settings
from app.events import on_startup, on_shutdown

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


def create_app() -> FastAPI:
    setup_logger()
    app = FastAPI(lifespan=setup_lifespan)

    setup_routers(app)
    return app