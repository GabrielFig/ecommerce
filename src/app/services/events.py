from fastapi.logger import logger

from app.database.base import close_db_connection
from app.database.base import on_db_init as postgres_on_db_init
from app.database.base import open_db_connection
from app.database.postgres import engine as postgres_engine


async def on_startup() -> None:
    logger.info("Connecting to Postgres database...")
    await open_db_connection(engine=postgres_engine, on_db_init=postgres_on_db_init)


async def on_shutdown() -> None:
    logger.info("Clossing Postgres database connection...")
    await close_db_connection(engine=postgres_engine)
