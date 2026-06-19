from uuid import UUID

from pydantic import BaseModel

from web_suffer.contexts.tasks.domain.types import SubmissionStatus


class SubmissionResponce(BaseModel):
    """
    Результат запроса получения отправления.

    submission_id: ID отправления.
    task_id: ID задания.
    user_ud: UD пользователя.
    content: Содержание отправления.
    file: название приложенного файла.
    status: Статус отправления "pending", "accepted" или "rejected".
    comment: Комментарий проверяющего.

    """

    submission_id: UUID
    task_id: UUID
    user_id: UUID
    content: str
    file: str | None = None
    status: SubmissionStatus
    comment: str
