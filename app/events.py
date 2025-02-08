from fastapi.logger import logger

from app.services.database.base import close_db_connection
from app.services.database.base import on_db_init as postgres_on_db_init
from app.services.database.base import open_db_connection
from app.services.database.mongo import close_connection as mongo_close_connection
from app.services.database.mongo import open_connection as mongo_connection
from app.services.database.postgres import engine as postgres_engine


async def on_startup() -> None:
    logger.info("Connecting to Postgres database...")
    await open_db_connection(engine=postgres_engine, on_db_init=postgres_on_db_init)

    logger.info("Connecting to MongoDB connection...")
    await mongo_connection()


async def on_shutdown() -> None:
    logger.info("Clossing Postgres database connection...")
    await close_db_connection(engine=postgres_engine)

    logger.info("Clossing MongoDB connection...")
    mongo_close_connection()
