from dataclasses import dataclass, field
from typing import Optional

from application.user.entity import UserEntity
from application.user.model import UserModel
from application.user.repository import UserRepository


@dataclass
class UserUpdateCommand:
    id: int
    username: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)


class UserUpdateUsecase:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, command: UserUpdateCommand) -> Optional[UserEntity]:
        user_model = await self.user_repository.get_by_id(command.id)
        if not user_model:
            return None
        if command.username:
            user_model.username = command.username
        if command.email:
            user_model.email = command.email
        await self.user_repository.update(user_model)
        return user_model.to_entity()
