from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TaskResponce(BaseModel):
    """
    Результат запроса получения задания.

    submission_id: ID отправления.
    task_id: ID задания.
    user_ud: UD пользователя.
    content: Содержание отправления.
    file: название приложенного файла.
    status: Статус отправления "pending", "accepted" или "rejected".
    comment: Комментарий проверяющего.

    """

    task_id: UUID
    title: str
    description: str
    deadline: datetime
    exp: int
    money: int
