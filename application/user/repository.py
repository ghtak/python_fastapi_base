from typing import Type, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.repository import BaseRepository
from application.user.model import User


class UserRepository(BaseRepository[User]):

    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def find_by_name(self, name: str) -> Sequence[User]:
        q = select(self.model).filter(User.username.like(f'%{name}%'))
        r = await self.session.execute(q)
        return r.scalars().all()
