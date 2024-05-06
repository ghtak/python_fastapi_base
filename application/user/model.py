from sqlalchemy.orm import Mapped, mapped_column

from core.database.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(index=True)
    email: Mapped[str]
