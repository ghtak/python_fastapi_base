from typing import Optional, Sequence

from fastapi import APIRouter

from application.user.depends import DependsCreateUserUsecase, DependsGetUserUsecase
from application.user.dto import UserResponse, CreateUserRequest
from application.user.usecase.create_user import CreateUserCommand
from application.user.usecase.get_user import GetUserCommand, GetUserKind

router = APIRouter(
    prefix="/user",
    tags=["/user"]
)


@router.get('/{user_id:int}', response_model=Optional[UserResponse])
async def get_app_state(user_id: int,
                        usecase: DependsGetUserUsecase):
    user = await usecase.execute(GetUserCommand(
        kind=GetUserKind.BY_ID,
        id=user_id))
    return user[0] if len(user) > 0 else None

@router.get('/', response_model=Sequence[UserResponse])
async def get_app_state(name: str,
                        usecase: DependsGetUserUsecase):
    users = await usecase.execute(GetUserCommand(
        kind=GetUserKind.BY_NAME,
        name=name))
    return users


@router.post('/', response_model=UserResponse)
async def create_user(user: CreateUserRequest,
                      usecase: DependsCreateUserUsecase):
    return await usecase.execute(CreateUserCommand(
        username=user.username,
        email=user.email
    ))
