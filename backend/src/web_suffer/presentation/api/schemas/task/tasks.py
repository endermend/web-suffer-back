from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from web_suffer.contexts.tasks.domain.types import TaskStatusType


class UserTaskResponce(BaseModel):
    """
    Результат запроса получения задания.

    task_id: ID отправления.
    title: Название задания.
    description: Описание задание.
    deadline: Время истечения задания.
    exp: опыт.
    money: монеты.
    status:  Статус лучшего отправления "pending", "accepted" или "rejected".

    """

    task_id: UUID
    title: str
    description: str
    deadline: datetime
    exp: int
    money: int
    status: TaskStatusType
