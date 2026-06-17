from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from web_suffer.contexts.tasks.domain.entities.submission import Submission
from web_suffer.contexts.tasks.domain.repository.submission_repository import ISubmissionRepository
from web_suffer.contexts.tasks.domain.value_objects.submission_id import SubmissionID
from web_suffer.contexts.tasks.domain.value_objects.submission_status import SubmissionStatus
from web_suffer.contexts.tasks.infrastructure.mappers.submission_orm_mapper import SubmissionORMMapper
from web_suffer.contexts.tasks.infrastructure.persistence.models.submission_model import SubmissionORMModel


class SubmissionRepository(ISubmissionRepository):
    """Реализация Submission репозитория."""

    def __init__(self, session: AsyncSession, mapper: SubmissionORMMapper) -> None:
        """Инициализация SubmissionRepository."""
        self._session = session
        self._mapper = mapper

    async def save(self, submission: Submission) -> None:
        """Сохранение Submission."""
        async with self._session.begin():
            submission_orm = await self._session.get(SubmissionORMModel, submission.id.value)

            if not submission_orm:
                submission_orm = SubmissionORMModel()

            self._mapper.update_from_domain(orm=submission_orm, entity=submission)
            self._session.add(submission_orm)

    async def get_by_id(self, submission_id: SubmissionID) -> Submission | None:
        """
        Получение Submission по SubmissionID.

        None, если submission не найден.

        Returns:
            Отправление по id.

        """
        submussion_orm = await self._session.get(SubmissionORMModel, submission_id.value)
        if not submussion_orm:
            return None
        return self._mapper.to_domain(orm=submussion_orm)

    async def get_list(self, status: SubmissionStatus | None = None) -> list[Submission]:
        """
        Получение Submission.

        Если submission_status не None, фильтрует по статусу

        Returns:
            Список отправлений.

        """
        stmt = select(SubmissionORMModel)
        if status:
            stmt = stmt.where(SubmissionORMModel.status == status)
        result = await self._session.execute(stmt)
        submissions_orm = result.scalars()
        return [self._mapper.to_domain(orm=submission_orm) for submission_orm in submissions_orm]
