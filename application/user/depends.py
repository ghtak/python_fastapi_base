from typing import Annotated

from fastapi import Depends

from application.user.repository import UserRepository
from application.user.usecase.create_user import CreateUserUsecase
from application.user.usecase.get_user import GetUserUsecase
from core.depends import DependsAsyncTransactionalSession, DependsAsyncScopedSession


async def get_create_user_usecase(session: DependsAsyncTransactionalSession) -> CreateUserUsecase:
    return CreateUserUsecase(UserRepository(session))


DependsCreateUserUsecase = Annotated[CreateUserUsecase, Depends(get_create_user_usecase)]


async def get_get_user_usecase(session: DependsAsyncScopedSession) -> GetUserUsecase:
    return GetUserUsecase(UserRepository(session))


DependsGetUserUsecase = Annotated[CreateUserUsecase, Depends(get_get_user_usecase)]
