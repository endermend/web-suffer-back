from pydantic import BaseModel

from web_suffer.contexts.tasks.domain.types import TaskStatus


class TaskStatisticsResponce(BaseModel):
    """
    Результат запроса получения задания.

    task_all: Общее число доступных заданий.
    task_status: Число доступных заданий по статусам.

    """

    task_all: int

    task_status: dict[TaskStatus, int] | None
