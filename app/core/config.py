import os
import sys
from functools import lru_cache
from typing import Any, Dict, Tuple, Type

import hvac
from fastapi.logger import logger
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

class Settings(BaseSettings):

    environment: str

    api_prefix: str

    pg_db_user: str
    pg_db_password: str
    pg_db_name: str
    pg_db_host: str
    pg_db_port: int

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # environment = os.getenv("ENVIRONMENT", None)
        # if environment is not None and environment != LOCAL_ENVIRONMENT:
        #     return (
        #         VaultSecretsSettingsSource(settings_cls),
        #         init_settings,
        #         env_settings,
        #         dotenv_settings,
        #         file_secret_settings,
        #     )
        return env_settings, dotenv_settings, file_secret_settings, init_settings

    @classmethod
    def init(cls) -> BaseSettings:
        try:
            logger.info("Initializing application settings.")
            return Settings()
        except Exception:
            logger.critical("Error Initializing application settings: ", exc_info=True)
            sys.exit(-1)


@lru_cache
def get_settings() -> Type[Settings]:
    return Settings.init()