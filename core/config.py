import os
from enum import Enum
from functools import lru_cache
from typing import Literal, Optional, Self

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Env(str, Enum):
    LOCAL = "local"
    DEV = "dev"
    STAGE = "stage"
    PROD = "prod"
    TEST = "test"


class Config(BaseSettings):
    model_config = ConfigDict(extra='allow')

    app_host: str
    app_port: int
    log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    log_dir: str
    cors_origin: Optional[list[str]]
    db_url: str

    @staticmethod
    @lru_cache
    def from_env() -> Self:
        return Config(
            _env_file=f'.env.{os.getenv("ENV", Env.LOCAL.value)}',
            _env_file_encoding="utf-8"
        )

