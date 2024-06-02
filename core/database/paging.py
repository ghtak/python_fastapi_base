import typing

from pydantic import BaseModel

DTOType = typing.TypeVar("DTOType")


class Paging(BaseModel, typing.Generic[DTOType]):
    total: int
    page: int
    items: typing.Optional[typing.Sequence[DTOType]]
