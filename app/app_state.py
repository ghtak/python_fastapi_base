import logging
from dataclasses import dataclass
from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Config
from app.database import Database


@dataclass
class AppState:
    config: Config
    database: Database

    def __init__(self, config: Config):
        self.config = config
        self.database = Database(config=config)

    def init_logging(self):
        logging.basicConfig(
            level=logging.getLevelName(self.config.log_level),
            datefmt='%Y/%m/%d %H:%M:%S',
            format='%(asctime)s|%(levelname)s|%(message)s',
        )


async def get_scoped_database_session(app_state: Annotated[AppState, Depends()]) \
        -> AsyncIterator[AsyncSession]:
    async with app_state.database.sessionmaker.begin() as session:
        yield session

    # async with app_state.database.session() as session:
    #     yield session


async def get_database_session(app_state: Annotated[AppState, Depends()]) -> AsyncSession:
    return app_state.database.sessionmaker()
