from datetime import UTC, datetime

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from web_suffer.contexts.tasks.domain.entities.task import Task
from web_suffer.contexts.tasks.domain.repository.task_repository import ITaskRepository
from web_suffer.contexts.tasks.domain.types import TaskOrderBy, TaskStatus, TaskStatusFilter
from web_suffer.contexts.tasks.domain.value_objects.task_id import TaskID
from web_suffer.contexts.tasks.infrastructure.mappers.task_orm_mapper import TaskORMMapper
from web_suffer.contexts.tasks.infrastructure.persistence.models.submission_model import SubmissionORMModel
from web_suffer.contexts.tasks.infrastructure.persistence.models.task_model import TaskORMModel
from web_suffer.shared.domain.value_objects.user_id import UserID

MIN_DATETIME = datetime.min.replace(tzinfo=UTC)


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
        stmt = select(TaskORMModel)
        if deadline_from is not None:
            stmt = stmt.where(TaskORMModel.deadline >= deadline_from)

        if deadline_till is not None:
            stmt = stmt.where(TaskORMModel.deadline <= deadline_till)

        if offset is not None:
            stmt = stmt.offset(offset)

        if limit is not None:
            stmt = stmt.limit(limit)

        result = await self._session.execute(stmt)
        tasks_orm = result.scalars()
        return [self._mapper.to_domain(orm=task_orm) for task_orm in tasks_orm]

    async def get_list(  # noqa: C901
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

        Returns:
            Список заданий.

        """
        status_stmt = select(
            SubmissionORMModel.status,
        ).where(
            and_(
                SubmissionORMModel.user_id == user_id.value,
                SubmissionORMModel.task_id == TaskORMModel.id,
            ),
        ).order_by(
            func.case(
                (SubmissionORMModel.status == "accepted", 1),
                (SubmissionORMModel.status == "pending", 2),
                (SubmissionORMModel.status == "rejected", 3),
                else_=4,
            ),
        ).limit(1).scalar_subquery()

        last_submission_stmt = select(
            func.max(SubmissionORMModel.created_at),
        ).where(
            and_(
                SubmissionORMModel.user_id == user_id.value,
                SubmissionORMModel.task_id == TaskORMModel.id,
            ),
        ).scalar_subquery()

        stmt = select(
            TaskORMModel,
            func.coalesce(status_stmt, "available").label("status"),
        )

        if status == "available":
            stmt = stmt.where(
                or_(
                    ~func.exists().where(
                        and_(
                            SubmissionORMModel.user_id == user_id.value,
                            SubmissionORMModel.task_id == TaskORMModel.id,
                        ),
                    ),
                    status_stmt == "rejected",
                ),
            )
        elif status == "pending":
            stmt = stmt.where(status_stmt == "pending")
        elif status == "accepted":
            stmt = stmt.where(status_stmt == "accepted")

        if deadline_from is not None:
            stmt = stmt.where(TaskORMModel.deadline >= deadline_from)

        if deadline_till is not None:
            stmt = stmt.where(TaskORMModel.deadline <= deadline_till)

        if order_by == "title":
            stmt = stmt.order_by(TaskORMModel.title)
        elif order_by == "deadline":
            stmt = stmt.order_by(TaskORMModel.deadline)
        elif order_by == "status":
            stmt = stmt.order_by(
                func.case(
                    (func.coalesce(status_stmt, "available") == "accepted", 1),
                    (func.coalesce(status_stmt, "available") == "pending", 2),
                    (func.coalesce(status_stmt, "available") == "rejected", 3),
                    (func.coalesce(status_stmt, "available") == "available", 4),
                    else_=5,
                ),
            )
        elif order_by == "last_submission":
            stmt = stmt.order_by(
                func.coalesce(last_submission_stmt, MIN_DATETIME).desc(),
            )

        stmt = stmt.order_by(TaskORMModel.id)

        if offset is not None:
            stmt = stmt.offset(offset)

        if limit is not None:
            stmt = stmt.limit(limit)

        result = await self._session.execute(stmt)
        tasks_orm = result.all()
        return [(self._mapper.to_domain(orm=task_orm), status) for task_orm, status in tasks_orm]
