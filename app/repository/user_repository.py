from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from . import BaseRepository
from app.model import User


class UserRepository(BaseRepository[User]):

    def __init__(self, session: AsyncSession):
        super().__init__(User, session)
