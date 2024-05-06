from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.app_state import AppState
from core.database.database import Database

AppStateDepends = Annotated[AppState, Depends()]


async def get_database(app_state: AppStateDepends) -> Database:
    return app_state.database


DatabaseDepends = Annotated[Database, Depends(get_database)]


async def get_transactional_session(database: DatabaseDepends) -> AsyncIterator[AsyncSession]:
    async with database.sessionmaker.begin() as session:
        yield session


async def get_scoped_session(database: DatabaseDepends) -> AsyncIterator[AsyncSession]:
    async with database.sessionmaker() as session:
        yield session


AsyncTransactionalSessionDepends = Annotated[AsyncSession, Depends(get_transactional_session)]
AsyncScopedSessionDepends = Annotated[AsyncSession, Depends(get_scoped_session)]