from collections.abc import AsyncIterable

from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from web_suffer.contexts.tasks.domain.repository.submission_repository import ISubmissionRepository
from web_suffer.contexts.tasks.domain.repository.task_repository import ITaskRepository
from web_suffer.contexts.tasks.domain.repository.user_repository import IUserTRepository
from web_suffer.contexts.tasks.infrastructure.mappers.submission_orm_mapper import SubmissionORMMapper
from web_suffer.contexts.tasks.infrastructure.mappers.task_orm_mapper import TaskORMMapper
from web_suffer.contexts.tasks.infrastructure.mappers.usert_orm_mapper import UserTORMMapper
from web_suffer.contexts.tasks.infrastructure.persistence.repositories.submission_repository import SubmissionRepository
from web_suffer.contexts.tasks.infrastructure.persistence.repositories.task_repository import TaskRepository
from web_suffer.contexts.tasks.infrastructure.persistence.repositories.user_repository import UserTRepository


class TaskDBProvider(Provider):
    """Провайдер бд заданий."""

    user_mapper = provide(
        UserTORMMapper,
        scope=Scope.APP,
    )

    task_mapper = provide(
        TaskORMMapper,
        scope=Scope.APP,
    )

    submission_mapper = provide(
        SubmissionORMMapper,
        scope=Scope.APP,
    )

    @provide(scope=Scope.REQUEST)
    @staticmethod
    async def get_user_repository(
        session: AsyncSession,
        mapper: UserTORMMapper,
    ) -> AsyncIterable[IUserTRepository]:
        """
        Провайдер репозитория пользователя.

        Yields:
            Iterator[AsyncIterable[IUserTRepository]]

        """
        yield UserTRepository(session=session, mapper=mapper)

    @provide(scope=Scope.REQUEST)
    @staticmethod
    async def get_task_repository(
        session: AsyncSession,
        mapper: TaskORMMapper,
    ) -> AsyncIterable[ITaskRepository]:
        """
        Провайдер репозитория заданий.

        Yields:
            Iterator[AsyncIterable[ITaskRepository]]

        """
        yield TaskRepository(session=session, mapper=mapper)

    @provide(scope=Scope.REQUEST)
    @staticmethod
    async def get_submission_repository(
        session: AsyncSession,
        mapper: SubmissionORMMapper,
    ) -> AsyncIterable[ISubmissionRepository]:
        """
        Провайдер репозитория отправлений.

        Yields:
            Iterator[AsyncIterable[ISubmissionRepository]]

        """
        yield SubmissionRepository(session=session, mapper=mapper)
