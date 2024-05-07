from typing import Type, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.repository import BaseRepository
from application.user.model import UserModel


class UserRepository(BaseRepository[UserModel]):

    def __init__(self, session: AsyncSession):
        super().__init__(UserModel, session)

    async def find_by_name(self, name: str) -> Sequence[UserModel]:
        q = select(self.model).filter(UserModel.username.like(f'%{name}%'))
        r = await self.session.execute(q)
        return r.scalars().all()
