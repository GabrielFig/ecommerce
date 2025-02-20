import sys
from datetime import datetime
from enum import Enum
from typing import Awaitable, Callable
from uuid import uuid4

import pytz

from fastapi.logger import logger
from sqlalchemy import String, select, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.config import get_settings


class BaseModel(AsyncAttrs, DeclarativeBase):
    pass


class MetadataMixin:

    class Status(str, Enum):
        disable = "0"
        enable = "1"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    created_by: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    create_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(pytz.utc)
    )
    update_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=datetime.now(pytz.utc),
        default=datetime.now(pytz.utc),
    )
    status: Mapped[str] = mapped_column(String(2), default=Status.enable.value)

    @property
    def create_date_with_timezone(self) -> datetime:
        return self.create_date.astimezone(tz=pytz.timezone(get_settings().timezone))

    @property
    def update_date_with_timezone(self) -> datetime:
        return self.update_date.astimezone(tz=pytz.timezone(get_settings().timezone))


async def open_db_connection(
    engine: AsyncEngine, on_db_init: Callable[[AsyncConnection], Awaitable[None]]
) -> None:
    try:
        async with engine.begin() as conn:
            await on_db_init(conn)
    except Exception:
        logger.critical("Error connecting to the database: ", exc_info=True)
        sys.exit(-1)


async def close_db_connection(engine: AsyncEngine) -> None:
    await engine.dispose()


async def check_db_connection(session: AsyncSession) -> None:
    try:
        result = await session.execute(select(1))
        logger.info(f"SELECT 1 result: {result.first()}")
    except Exception:
        logger.error(
            "An error ocurred while checking database connection: ", exc_info=True
        )


async def on_db_init(conn: AsyncConnection) -> None:
    if get_settings().environment == "local":
        logger.info("Creating tables for the local environment...")
        await conn.run_sync(BaseModel.metadata.create_all)
