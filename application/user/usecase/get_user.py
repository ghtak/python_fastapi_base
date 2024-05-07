from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from application.user.entity import User as UserEntity
from application.user.repository import UserRepository


class GetUserKind(int, Enum):
    BY_ID = 0
    BY_NAME = 1


@dataclass
class GetUserCommand:
    kind: GetUserKind
    id: Optional[int] = field(default=None)
    name: Optional[str] = field(default=None)


class GetUserUsecase:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, command: GetUserCommand) -> list[UserEntity]:
        users = []
        if command.kind == GetUserKind.BY_ID:
            user_model = await self.user_repository.get_by_id(command.id)
            if user_model is not None:
                users.append(user_model.to_entity())
        elif command.kind == GetUserKind.BY_NAME:
            selected = await self.user_repository.find_by_name(
                command.name)
            users.extend(map(lambda x: x.to_entity(), selected))
        return users
