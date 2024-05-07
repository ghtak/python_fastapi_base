from dataclasses import dataclass

from application.user.entity import UserEntity
from application.user.model import UserModel
from application.user.repository import UserRepository


@dataclass
class UserCreateCommand:
    username: str
    email: str


class UserCreateUsecase:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, command: UserCreateCommand) -> UserEntity:
        user_model = await self.user_repository.create(
            UserModel.from_dict(command.__dict__))
        return user_model.to_entity()
