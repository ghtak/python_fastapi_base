from typing import Self

from sqlalchemy.orm import Mapped, mapped_column

from core.database.database import Base
from application.user.entity import User as UserEntity


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(index=True)
    email: Mapped[str]

    @classmethod
    def from_dict(cls, objs: dict) -> Self:
        return User(**objs)

    def to_entity(self) -> UserEntity:
        return UserEntity(
            **self.__dict__
        )

