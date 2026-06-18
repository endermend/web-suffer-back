from collections.abc import AsyncIterable

from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from web_suffer.contexts.auth.domain.repositories.user_repository import (
    IUserRepository,
)
from web_suffer.contexts.auth.infrastructure.mappers.user_orm_mapper import UserORMMapper
from web_suffer.contexts.auth.infrastructure.persistence.repositories import (
    UserRepository,
)


class AuthDBProvider(Provider):
    """Провайдер бд авторизации."""

    mapper = provide(
        UserORMMapper,
        scope=Scope.APP,
    )

    @provide(scope=Scope.REQUEST)
    @staticmethod
    async def get_user_repository(
        session: AsyncSession,
        mapper: UserORMMapper,
    ) -> AsyncIterable[IUserRepository]:
        """
        Провайдер репозитория пользователя.

        Yields:
            Iterator[AsyncIterable[IUserRepository]]

        """
        yield UserRepository(session=session, mapper=mapper)
