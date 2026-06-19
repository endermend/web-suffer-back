from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from web_suffer.shared.infrastructure.models.base_model import Base


class UserORMModel(Base):
    """ORM Модель пользователя."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self) -> str:  # noqa: D105
        return f"<UserModel(id={self.id}, email={self.email}, role={self.role})>"
