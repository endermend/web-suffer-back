from abc import abstractmethod
from datetime import datetime
from typing import Protocol

from web_suffer.contexts.tasks.domain.entities.task import Task
from web_suffer.contexts.tasks.domain.types import TaskOrderBy, TaskStatus, TaskStatusFilter
from web_suffer.contexts.tasks.domain.value_objects.task_id import TaskID
from web_suffer.shared.domain.value_objects.user_id import UserID


class ITaskRepository(Protocol):
    """Протокол Task репозитория."""

    @abstractmethod
    async def save(self, task: Task) -> None:
        """Сохранение Task."""

    @abstractmethod
    async def get_by_id(self, task_id: TaskID) -> Task | None:
        """
        Получение Task по TaskID.

        None, если task не найден.
        """

    @abstractmethod
    async def get_unathorized_list(
        self,
        deadline_from: datetime | None = None,
        deadline_till: datetime | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Task]:
        """
        Получение списка заданий без пользователя.

        Returns:
            list[Task] - список заданий.

        """

    @abstractmethod
    async def get_list(
        self,
        user_id: UserID,
        deadline_from: datetime | None = None,
        deadline_till: datetime | None = None,
        status: TaskStatusFilter | None = None,
        order_by: TaskOrderBy | None = None,
        limit: int | None = None,
        offset: int | None = None,
        ) -> list[tuple[Task, TaskStatus]]:
        """
        Получение Tasks.

        Если before не None, фильтрует по параметрам.
        """
