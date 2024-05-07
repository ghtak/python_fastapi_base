from typing import Optional, Sequence

from fastapi import APIRouter

from application.user.depends import DependsUserCreateUsecase, DependsUserGetUsecase, DependsUserUpdateUsecase
from application.user.dto import UserDto, UserCreateDto, UserUpdateDto
from application.user.usecase.user_create import UserCreateCommand
from application.user.usecase.user_get import UserGetCommand
from application.user.usecase.user_udpate import UserUpdateCommand

router = APIRouter(
    prefix="/user",
    tags=["/user"]
)


@router.get('/{user_id:int}', response_model=Optional[UserDto])
async def user_get_by_id(user_id: int,
                         usecase: DependsUserGetUsecase):
    user = await usecase.execute(UserGetCommand.by_id(user_id))
    return user[0] if len(user) > 0 else None


@router.get('/', response_model=Sequence[UserDto])
async def user_get_by_name(name: str,
                           usecase: DependsUserGetUsecase):
    return await usecase.execute(UserGetCommand.by_name(name))


@router.post('/', response_model=UserDto)
async def user_create(user: UserCreateDto,
                      usecase: DependsUserCreateUsecase):
    return await usecase.execute(UserCreateCommand(
        username=user.username,
        email=user.email
    ))


@router.put('/{user_id:int}', response_model=Optional[UserDto])
async def user_update(
        user_id: int,
        user_update: UserUpdateDto,
        usecase: DependsUserUpdateUsecase
):
    return await usecase.execute(
        UserUpdateCommand(id=user_id,
                          **user_update.__dict__)
    )

# async def user_update(
#         user_id: int,
#         user_update: UserUpdateDto,
#         session: DependsAsyncTransactionalSession
# ):
#     repo = UserRepository(session)
#     model = await repo.get_by_id(user_id)
#     if user_update.username:
#         model.username = user_update.username
#     if user_update.email:
#         model.email = user_update.email
#     await repo.update(model)
#     return model
