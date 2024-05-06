from pydantic import BaseModel, ConfigDict

from application.user.entity import User


class UserResponse(User):
    pass


class CreateUserRequest(BaseModel):
    username: str
    email: str
