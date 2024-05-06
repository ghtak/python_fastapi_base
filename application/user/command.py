from dataclasses import dataclass

from application.user.dto import CreateUserRequest


@dataclass
class CreateUserCommand:
    user: CreateUserRequest
