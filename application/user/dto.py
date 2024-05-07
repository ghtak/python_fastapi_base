from pydantic import BaseModel, ConfigDict

from application.user.entity import UserEntity


class UserDto(UserEntity):
    pass


class UserCreateDto(BaseModel):
    username: str
    email: str
