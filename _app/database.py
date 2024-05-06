import contextlib
from typing import AsyncIterator, Annotated, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncConnection
from sqlalchemy.ext.asyncio.session import AsyncSession

from _app.config import Config
from _app.model import Base


class Database:
    engine: AsyncEngine
    sessionmaker: async_sessionmaker

    def __init__(self, config: Any):
        self.engine = create_async_engine(
            url=config.db_url,
        )
        self.sessionmaker = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        async with self.engine.begin() as con:
            try:
                yield con
            except Exception:
                await con.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        session = self.sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def init_models(self, drop: bool = False):
        async with self.connect() as conn:
            if drop:
                await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


DatabaseDepends = Annotated[Database, Depends()]


async def get_transactional_session(database: DatabaseDepends) -> AsyncIterator[AsyncSession]:
    async with database.sessionmaker.begin() as session:
        yield session

    # async with core.database.session() as session:
    #     yield session


async def get_scoped_session(database: DatabaseDepends) -> AsyncIterator[AsyncSession]:
    async with database.sessionmaker() as session:
        yield session


AsyncTransactionalSessionDepends = Annotated[AsyncSession, Depends(get_transactional_session)]
AsyncScopedSessionDepends = Annotated[AsyncSession, Depends(get_scoped_session)]
