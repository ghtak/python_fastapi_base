from typing import Optional

from fastapi import APIRouter

from application.user.dto import UserResponse, CreateUserRequest
from application.user.repository import UserRepository
from application.user.usecase.create_user import CreateUser, CreateUserCommand
from core.depends import AsyncTransactionalSessionDepends, AsyncScopedSessionDepends

router = APIRouter(
    prefix="/user",
    tags=["/user"]
)


@router.get('/{user_id:int}', response_model=Optional[UserResponse])
async def get_app_state(user_id: int):
    return user_id


@router.post('/')
async def create_user(user: CreateUserRequest,
                      session: AsyncTransactionalSessionDepends):
    usecase = CreateUser(UserRepository(session))
    command = CreateUserCommand(user=user)
    return await usecase.execute(command)
