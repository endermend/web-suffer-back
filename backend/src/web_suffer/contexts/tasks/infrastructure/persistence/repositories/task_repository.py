from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from web_suffer.contexts.tasks.domain.entities.task import Task
from web_suffer.contexts.tasks.domain.repository.task_repository import ITaskRepository
from web_suffer.contexts.tasks.domain.value_objects.task_id import TaskID
from web_suffer.contexts.tasks.infrastructure.mappers.task_orm_mapper import TaskORMMapper
from web_suffer.contexts.tasks.infrastructure.persistence.models.task_model import TaskORMModel


class TaskRepository(ITaskRepository):
    """Реализация Task репозитория."""

    def __init__(self, session: AsyncSession, mapper: TaskORMMapper) -> None:
        """Инициализация TaskRepository."""
        self._session = session
        self._mapper = mapper

    async def save(self, task: Task) -> None:
        """Сохранение Task."""
        async with self._session.begin():
            task_orm = await self._session.get(TaskORMModel, task.id.value)

            if not task_orm:
                task_orm = TaskORMModel()

            self._mapper.update_from_domain(orm=task_orm, entity=task)
            self._session.add(task_orm)

    async def get_by_id(self, task_id: TaskID) -> Task | None:
        """
        Получение Task по TaskID.

        None, если task не найден.

        Returns:
            Задание по id.

        """
        task_orm = await self._session.get(TaskORMModel, task_id.value)
        if not task_orm:
            return None
        return self._mapper.to_domain(orm=task_orm)

    async def get_list(self, before: datetime | None = None) -> list[Task]:
        """
        Получение Tasks.

        Если before не None, фильтрует по дедлайнду задания до before

        Returns:
            Список заданий.

        """
        stmt = select(TaskORMModel)
        if before:
            stmt = stmt.where(TaskORMModel.deadline <= before)
        result = await self._session.execute(stmt)
        tasks_orm = result.scalars()
        return [self._mapper.to_domain(orm=task_orm) for task_orm in tasks_orm]
