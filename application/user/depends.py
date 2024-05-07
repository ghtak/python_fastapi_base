from typing import Annotated

from fastapi import Depends

from application.user.repository import UserRepository
from application.user.usecase.user_create import UserCreateUsecase
from application.user.usecase.user_get import UserGetUsecase
from application.user.usecase.user_udpate import UserUpdateUsecase
from core.depends import DependsAsyncTransactionalSession, DependsAsyncScopedSession


async def user_create_usecase(session: DependsAsyncTransactionalSession) -> UserCreateUsecase:
    return UserCreateUsecase(UserRepository(session))


DependsUserCreateUsecase = Annotated[UserCreateUsecase, Depends(user_create_usecase)]


async def user_get_usecase(session: DependsAsyncScopedSession) -> UserGetUsecase:
    return UserGetUsecase(UserRepository(session))


DependsUserGetUsecase = Annotated[UserGetUsecase, Depends(user_get_usecase)]


async def user_update_usecase(session: DependsAsyncScopedSession) -> UserUpdateUsecase:
    return UserUpdateUsecase(UserRepository(session))


DependsUserUpdateUsecase = Annotated[UserUpdateUsecase, Depends(user_update_usecase)]
