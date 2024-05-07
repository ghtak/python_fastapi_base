from typing import Optional, Sequence

from fastapi import APIRouter

from application.user.depends import DependsUserCreateUsecase, DependsUserGetUsecase
from application.user.dto import UserDto, UserCreateDto
from application.user.usecase.user_create import UserCreateCommand
from application.user.usecase.user_get import UserGetCommand, UserGetKind

router = APIRouter(
    prefix="/user",
    tags=["/user"]
)


@router.get('/{user_id:int}', response_model=Optional[UserDto])
async def user_get_by_id(user_id: int,
                         usecase: DependsUserGetUsecase):
    user = await usecase.execute(UserGetCommand(
        kind=UserGetKind.BY_ID,
        id=user_id))
    return user[0] if len(user) > 0 else None


@router.get('/', response_model=Sequence[UserDto])
async def user_get_by_name(name: str,
                           usecase: DependsUserGetUsecase):
    users = await usecase.execute(UserGetCommand(
        kind=UserGetKind.BY_NAME,
        name=name))
    return users


@router.post('/', response_model=UserDto)
async def user_create(user: UserCreateDto,
                      usecase: DependsUserCreateUsecase):
    return await usecase.execute(UserCreateCommand(
        username=user.username,
        email=user.email
    ))
