from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TaskResponce(BaseModel):
    """
    Результат запроса получения задания.

    task_id: ID отправления.
    title: Название задания.
    description: Описание задание.
    deadline: Время истечения задания.
    exp: опыт.
    money: монеты.

    """

    task_id: UUID
    title: str
    description: str
    deadline: datetime
    exp: int
    money: int
