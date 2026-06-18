from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from web_suffer.shared.infrastructure.models.base_model import Base


class UserTORMModel(Base):
    """ORM Модель пользователя."""

    __tablename__ = "users_t"

    exp: Mapped[int] = mapped_column(Integer, nullable=False)
    money: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self) -> str:  # noqa: D105
        return f"<UserTModel(id={self.id}, exp={self.exp}, money={self.money})>"
