import asyncio

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.config import get_settings

engine: AsyncEngine = create_async_engine(
    URL.create(
        "postgresql+asyncpg",
        username=get_settings().pg_db_user,
        password=get_settings().pg_db_password,
        host=get_settings().pg_db_host,
        port=get_settings().pg_db_port,
        database=get_settings().pg_db_name,
    ),
    echo=get_settings().debug,
)

async_session: async_sessionmaker[AsyncSession] = async_scoped_session(
    async_sessionmaker(bind=engine, expire_on_commit=False), asyncio.current_task
)
