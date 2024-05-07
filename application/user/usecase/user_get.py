from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Self, Sequence

from application.user.entity import UserEntity
from application.user.repository import UserRepository


class UserGetKind(int, Enum):
    BY_ID = 0
    BY_NAME = 1


@dataclass
class UserGetCommand:
    kind: UserGetKind
    id: Optional[int] = field(default=None)
    name: Optional[str] = field(default=None)

    @classmethod
    def by_id(cls, id_: int) -> Self:
        return cls(kind=UserGetKind.BY_ID, id=id_)

    @classmethod
    def by_name(cls, name: str) -> Self:
        return cls(kind=UserGetKind.BY_NAME, name=name)


class UserGetUsecase:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, command: UserGetCommand) -> Sequence[UserEntity]:
        if command.kind == UserGetKind.BY_ID:
            user_entity = await self.get_by_id(command.id)
            return [user_entity] if user_entity else []
        elif command.kind == UserGetKind.BY_NAME:
            return await self.find_by_name(command.name)
        return []

    async def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        user_model = await self.user_repository.get_by_id(user_id)
        return user_model.to_entity() if user_model else None

    async def find_by_name(self, name: str) -> Sequence[UserEntity]:
        selected = await self.user_repository.find_by_name(name)
        return list(map(lambda x: x.to_entity(), selected))
