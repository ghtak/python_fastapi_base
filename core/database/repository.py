from typing import TypeVar, Generic, Type, Optional, Sequence

from sqlalchemy import select, func, Select
from sqlalchemy.ext.asyncio import AsyncSession

from core.dto import Paging

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    model: Type[ModelType]
    session: AsyncSession

    def __init__(self,
                 model: Type[ModelType],
                 session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, model_id: int) -> Optional[ModelType]:
        if hasattr(self.model, 'id'):
            q = select(self.model).where(self.model.id == model_id)
            r = await self.session.execute(q)
            return r.scalars().first()
        return None

    async def create(self, model: ModelType) -> ModelType:
        self.session.add(model)
        await self.session.flush()
        return model

    async def update(self, model: ModelType):
        await self.session.merge(model)
        await self.session.flush()
        return model

    async def count(self, *criteria):
        r = await self.session.execute(
            select(func.count()).select_from(self.model).filter(*criteria)
        )
        return r.scalar_one()

    async def paginate(self, q: Select, page: int, count: int) -> Sequence[ModelType]:
        assert page > 0
        assert count > 0
        r = await self.session.execute(
            q.limit(count).offset((page - 1) * count)
        )
        return r.scalars().all()


    # async def find_by(self, **kwargs: dict[str, Any]) -> list[ModelType]:
    #     for k,v in kwargs:
    #
    #     return []
