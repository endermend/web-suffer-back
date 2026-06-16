from collections.abc import AsyncIterable

from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from web_suffer.contexts.auth.domain.repositories.user_repository import (
    IUserRepository,
)
from web_suffer.contexts.auth.infrastructure.mappers.user_orm_mapper import UserORMMapper
from web_suffer.contexts.auth.infrastructure.persistence.repositories import (
    UserRepository,
)
from web_suffer.infrastructure.config import Config
from web_suffer.shared.infrastructure.persistence.session import (
    new_async_session_maker,
)


class DBProvider(Provider):
    """Провайдер для всего связанного с БД."""  # noqa: RUF002

    mapper = provide(
        UserORMMapper,
        scope=Scope.APP,
    )

    @provide(scope=Scope.APP)
    @staticmethod
    def get_session_maker(config: Config) -> async_sessionmaker[AsyncSession]:
        """
        Провайдер для async_sessionmaker[AsyncSession].

        Returns:
            async_sessionmaker[AsyncSession]

        """
        return new_async_session_maker(db_config=config.DB)

    @provide(scope=Scope.REQUEST)
    @staticmethod
    async def get_session(
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        """
        Провайдер сессии.

        Yields:
            Iterator[AsyncIterable[AsyncSession]]

        """
        async with session_maker() as session:
            yield session

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
