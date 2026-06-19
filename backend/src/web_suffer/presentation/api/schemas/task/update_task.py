from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UpdateTaskRequest(BaseModel):
    """
    Входные данные изменения задания.

    task_id: Если не указано, создается новое задание.
    title: Оглавление задания.
    description: Описание задания.
    deadline: Дата и время истечения задания
    exp: опыт за задание.
    money: монеты за задание.
    """

    task_id: UUID | None = None
    title: str
    description: str
    deadline: datetime
    exp: int
    money: int


class UpdateTaskResponse(BaseModel):
    """
    Выходные данные создания задания.

    ID нового или измененного задания.
    """

    task_id: UUID
