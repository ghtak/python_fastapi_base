import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine, AsyncConnection, AsyncSession
from sqlalchemy.orm import declarative_base

from core.config import Config

Base = declarative_base()


class Database:
    engine: AsyncEngine
    sessionmaker: async_sessionmaker

    def __init__(self):
        config = Config.from_env()
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
            # session.commit()
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
