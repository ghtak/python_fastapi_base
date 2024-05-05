import os
from typing import Literal, Optional

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    app_host: str
    app_port: int
    env: Literal['dev', 'prod']
    log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    cors_origin: Optional[list[str]]

    @classmethod
    def from_env(cls):
        return Config(
            _env_file=os.getenv("ENV_FILE", ".env.local"),
            _env_file_encoding="utf-8"
        )