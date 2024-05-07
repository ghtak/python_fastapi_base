from dataclasses import dataclass

from application.user.entity import User as UserEntity
from application.user.model import User as UserModel
from application.user.repository import UserRepository


@dataclass
class CreateUserCommand:
    username: str
    email: str


class CreateUserUsecase:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, command: CreateUserCommand) -> UserEntity:
        user_model = await self.user_repository.create(
            UserModel.from_dict(command.__dict__))
        return user_model.to_entity()
