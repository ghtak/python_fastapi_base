import os
from typing import Literal

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    app_host: str
    app_port: int
    env: str

    log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    cors_origin: str | None


config = Config(
    _env_file=os.getenv("ENV_FILE", ".env.local"),
    _env_file_encoding="utf-8"
)
