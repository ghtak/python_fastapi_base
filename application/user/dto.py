from typing import Optional

from pydantic import BaseModel, Field

from application.user.entity import UserEntity
from core.database.paging import Paging


class UserDto(UserEntity):
    pass


class UserCreateDto(BaseModel):
    username: str
    email: str


class UserUpdateDto(BaseModel):
    username: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)


UserDtoPaging = Paging[UserDto]
