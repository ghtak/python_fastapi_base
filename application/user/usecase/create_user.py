from application.user.command import CreateUserCommand
from application.user.dto import UserResponse
from application.user.model import User
from application.user.repository import UserRepository


class CreateUser:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, command: CreateUserCommand) -> None:
        # return UserResponse(
        #     id=1,
        #     **command.user.__dict__
        # )
        await self.user_repository.create(
            User(**command.user.__dict__)
        )
