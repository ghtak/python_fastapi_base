from typing import Optional, Sequence

from fastapi import APIRouter

from application.user.depends import DependsUserCreateUsecase, DependsUserGetUsecase, DependsUserUpdateUsecase
from application.user.dto import UserDto, UserCreateDto, UserUpdateDto
from application.user.usecase.user_create import UserCreateCommand
from application.user.usecase.user_udpate import UserUpdateCommand
from core.dto import Paging
from core.logging_route import LoggingRoute

router = APIRouter(
    prefix="/user",
    tags=["/user"],
    route_class=LoggingRoute
)


@router.get("/", response_model=Paging[UserDto])
async def user_list(
        usecase: DependsUserGetUsecase,
        page: int,
        count: int,
):
    return await usecase.users(page, count)


@router.get('/{user_id:int}', response_model=Optional[UserDto])
async def user_get_by_id(user_id: int,
                         usecase: DependsUserGetUsecase):
    return await usecase.get_by_id(user_id)


@router.get('/{name:str}', response_model=Paging[UserDto])
async def user_get_by_name(name: str,
                           page: int,
                           count: int,
                           usecase: DependsUserGetUsecase):
    return await usecase.find_by_name(name, page, count)


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
