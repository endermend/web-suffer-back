from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from web_suffer.contexts.tasks.domain.entities.submission import Submission
from web_suffer.contexts.tasks.domain.repository.submission_repository import ISubmissionRepository
from web_suffer.contexts.tasks.domain.types import SubmissionOrderBy
from web_suffer.contexts.tasks.domain.value_objects.submission_id import SubmissionID
from web_suffer.contexts.tasks.domain.value_objects.submission_status import SubmissionStatus
from web_suffer.contexts.tasks.infrastructure.mappers.submission_orm_mapper import SubmissionORMMapper
from web_suffer.contexts.tasks.infrastructure.persistence.models.submission_model import SubmissionORMModel
from web_suffer.contexts.tasks.infrastructure.persistence.models.task_model import TaskORMModel
from web_suffer.shared.domain.value_objects.user_id import UserID


class SubmissionRepository(ISubmissionRepository):
    """Реализация Submission репозитория."""

    def __init__(self, session: AsyncSession, mapper: SubmissionORMMapper) -> None:
        """Инициализация SubmissionRepository."""
        self._session = session
        self._mapper = mapper

    @override
    async def save(self, submission: Submission) -> None:
        """Сохранение Submission."""
        async with self._session.begin():
            submission_orm = await self._session.get(SubmissionORMModel, submission.id.value)

            if not submission_orm:
                submission_orm = SubmissionORMModel()

            self._mapper.update_from_domain(orm=submission_orm, entity=submission)
            self._session.add(submission_orm)

    @override
    async def get_by_id(self, submission_id: SubmissionID) -> Submission | None:
        """
        Получение Submission по SubmissionID.

        None, если submission не найден.

        Returns:
            Отправление по id.

        """
        submission_orm = await self._session.get(SubmissionORMModel, submission_id.value)
        if not submission_orm:
            return None
        return self._mapper.to_domain(orm=submission_orm)

    @override
    async def get_list(
        self,
        user_id: UserID | None,
        status: SubmissionStatus | None = None,
        order_by: SubmissionOrderBy | None = None,
    ) -> list[Submission]:
        """
        Получение Submission.

        Если submission_status не None, фильтрует по статусу

        Returns:
            Упорядоченные отправления.

        """
        stmt = select(SubmissionORMModel)
        if user_id:
            stmt = stmt.where(SubmissionORMModel.user_id == user_id.value)
        if status:
            stmt = stmt.where(SubmissionORMModel.status == status.value)

        if order_by == "created_at":
            stmt = stmt.order_by(SubmissionORMModel.created_at)
        elif order_by == "status":
            stmt = stmt.order_by(SubmissionORMModel.status)
        elif order_by == "task_title":
            stmt = stmt.join(TaskORMModel).order_by(TaskORMModel.title)

        stmt = stmt.order_by(SubmissionORMModel.id)

        result = await self._session.execute(stmt)
        submissions_orm = result.scalars()
        return [self._mapper.to_domain(orm=submission_orm) for submission_orm in submissions_orm]
