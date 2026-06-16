import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from web_suffer.shared.infrastructure.models.base_model import Base


class SubmissionORMModel(Base):
    """ORM Модель задания."""

    __tablename__ = "submissions"

    task_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    file: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False)
    admin_comment: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:  # noqa: D105
        return f"<SubmissionkModel(id={self.id}, task_id={self.task_id}, user_id={self.user_id})>"
