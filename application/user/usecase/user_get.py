from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Self, Sequence

from sqlalchemy import Select

from application.user.entity import UserEntity
from application.user.model import UserModel
from application.user.repository import UserRepository
from core.dto import Paging


class UserGetUsecase:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def users(self, page: int, count: int):
        assert page > 0 and count > 0
        total, selected = await self.user_repository.users(page, count)
        return Paging[UserEntity](
            total=total,
            page=page,
            items=list(map(lambda x: UserEntity.model_validate(x), selected))
        )

    async def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        user_model = await self.user_repository.get_by_id(user_id)
        return UserEntity.model_validate(user_model) if user_model else None

    async def find_by_name(self, name: str, page: int, count: int) -> Paging[UserEntity]:
        assert page > 0 and count > 0

        total, selected = await self.user_repository.find_by_name(name, page, count)
        return Paging[UserEntity](
            total=total,
            page=page,
            items=list(map(lambda x: UserEntity.model_validate(x), selected))
        )
