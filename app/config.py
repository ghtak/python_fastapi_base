import os
from enum import Enum
from typing import Literal, Optional

from pydantic_settings import BaseSettings


class Env(str, Enum):
    LOCAL = "local"
    DEV = "dev"
    STAGE = "stage"
    PROD = "prod"


class Config(BaseSettings):
    app_host: str
    app_port: int
    env: Literal[Env.LOCAL, Env.DEV, Env.STAGE, Env.PROD]
    log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    cors_origin: Optional[list[str]]
    db_url: str

    @classmethod
    def from_env(cls):
        return Config(
            _env_file=os.getenv("ENV_FILE", ".env.local"),
            _env_file_encoding="utf-8"
        )
