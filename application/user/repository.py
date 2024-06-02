from typing import Type, Sequence

from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.repository import BaseRepository
from application.user.model import UserModel


class UserRepository(BaseRepository[UserModel]):

    def __init__(self, session: AsyncSession):
        super().__init__(UserModel, session)

    async def find_by_name(self, name: str, page: int, count: int):
        q = select(self.model).filter(UserModel.username.like(f'%{name}%'))
        total = await self.count(q)
        selected = await self.paginate(q, page, count)
        return total, selected

    async def users(self, page: int, count: int, *orders):
        total = await self.count()
        q = Select(self.model)
        if len(orders) > 0:
            q = q.order_by(*orders)
        else:
            q = q.order_by(self.model.id.desc())
        selected = await self.paginate(q, page, count)
        return total, selected
