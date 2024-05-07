import contextlib
from typing import AsyncIterator

from sqlalchemy import Insert, Update, Delete
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine, AsyncConnection, AsyncSession
from sqlalchemy.orm import declarative_base, Session

from core.config import Config

Base = declarative_base()


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        if self._flushing or isinstance(clause, (Insert, Update, Delete)):
            return Database.primary_engine.sync_engine
        return Database.secondary_engine.sync_engine


class Database:
    primary_engine: AsyncEngine
    secondary_engine: AsyncEngine
    sessionmaker: async_sessionmaker

    @classmethod
    def init(cls, config: Config):
        Database.primary_engine = create_async_engine(url=config.primary_db_url,
                                                      echo=True)
        Database.secondary_engine = create_async_engine(url=config.secondary_db_url,
                                                        echo=True)
        Database.sessionmaker = async_sessionmaker(
            sync_session_class=RoutingSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )

    @classmethod
    @contextlib.asynccontextmanager
    async def connect(cls) -> AsyncIterator[AsyncConnection]:
        async with cls.primary_engine.begin() as con:
            try:
                yield con
            except Exception:
                await con.rollback()
                raise

    @classmethod
    @contextlib.asynccontextmanager
    async def session(cls) -> AsyncIterator[AsyncSession]:
        session = cls.sessionmaker()
        try:
            yield session
            # session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    @classmethod
    async def sync_models(cls, drop: bool = False):
        # import application models for sync
        async with cls.connect() as conn:
            if drop:
                await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
