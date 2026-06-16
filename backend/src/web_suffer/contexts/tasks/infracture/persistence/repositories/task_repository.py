from web_suffer.contexts.tasks.domain.entities.task import Task
from web_suffer.contexts.tasks.domain.repository.task_repository import ITaskRepository
from web_suffer.contexts.tasks.domain.value_objects.task_id import TaskID
from web_suffer.contexts.tasks.domain.value_objects.task_status import TaskStatus


class TaskRepository(ITaskRepository):
    """Реализация Task репозитория."""

    async def save(self, task: Task) -> None:
        """Сохранение Task."""

    async def get_task_by_id(self, task_id: TaskID) -> Task | None:
        """
        Получение Task по TaskID.

        None, если task не найден.
        """

    async def get_tasks_list(self, task_status: TaskStatus | None = None) -> list[Task]:
        """
        Получение Tasks.

        Если task_status не None, фильтрует по статусу
        """
