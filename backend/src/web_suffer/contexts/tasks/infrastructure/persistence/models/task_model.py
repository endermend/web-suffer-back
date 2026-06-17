from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from web_suffer.shared.infrastructure.models.base_model import Base


class TaskORMModel(Base):
    """ORM Модель задания."""

    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    exp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    money: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    def __repr__(self) -> str:  # noqa: D105
        return f"<TaskModel(id={self.id}, title={self.title}, deadline={self.deadline})>"
