from abc import abstractmethod
from typing import Protocol

from web_suffer.contexts.tasks.domain.entities.task import Task
from web_suffer.contexts.tasks.domain.value_objects.task_id import TaskID


class ITaskRepository(Protocol):
    """Протокол Task репозитория."""

    @abstractmethod
    async def save(self, task: Task) -> None:
        """Сохранение Task."""

    @abstractmethod
    async def get_task_by_id(self, task_id: TaskID) -> Task | None:
        """
        Получение Task по TaskID.

        None, если task не найден.
        """
