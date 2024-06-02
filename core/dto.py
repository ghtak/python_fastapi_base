import typing

from pydantic import BaseModel

T = typing.TypeVar("T")


class Paging(BaseModel, typing.Generic[T]):
    total: int
    page: int
    items: typing.Optional[typing.List[T]]
