from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from web_suffer.contexts.auth.domain.entities import User
from web_suffer.contexts.auth.domain.repositories import IUserRepository
from web_suffer.contexts.auth.domain.value_objects import (
    PasswordHash,
    UserEmail,
)
from web_suffer.contexts.auth.infrastructure.persistence.models import UserORM
from web_suffer.shared.domain.value_objects import UserID


class UserRepository(IUserRepository):
    """Реализация IUserRepository на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        """Инициализация UserRepository."""
        self._session = session

    async def save(self, user: User) -> None:
        """Сохранение User."""
        user_orm = self._domain_to_orm(user_domain=user)
        self._session.add(user_orm)
        await self._session.commit()

    async def user_exists_by_email(self, email: UserEmail) -> bool:
        """
        Проверка существования User по UserEmail.

        Returns:
            bool: True если существует, False иначе

        """
        stmt = select(UserORM).where(UserORM.email == email.value)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def get_user_by_email(self, email: UserEmail) -> User | None:
        """
        Получение User по UserEmail.

        Returns:
            User | None: None если пользователь не найден.

        """
        stmt = select(UserORM).where(UserORM.email == email.value)
        result = await self._session.execute(stmt)
        user_orm = result.scalar()
        if user_orm is None:
            return None
        return self._orm_to_domain(user_orm=user_orm)

    async def get_user_by_id(self, user_id: UserID) -> User | None:
        """
        Получение User по UserId.

        Returns:
            Пользователь, если пользователь с таким ID существует, иначе None.

        """  # noqa: RUF002
        stmt = select(UserORM).where(UserORM.id == user_id.value)
        result = await self._session.execute(stmt)
        user_orm = result.scalar()
        if user_orm is None:
            return None
        return self._orm_to_domain(user_orm=user_orm)

    @staticmethod
    def _domain_to_orm(user_domain: User) -> UserORM:
        user_orm = UserORM()
        user_orm.id = user_domain.id.value
        user_orm.email = user_domain.email.value
        user_orm.password_hash = user_domain.password_hash.value
        return user_orm

    @staticmethod
    def _orm_to_domain(user_orm: UserORM) -> User:
        return User(
            id=UserID(user_orm.id),
            email=UserEmail(user_orm.email),
            password_hash=PasswordHash(user_orm.password_hash),
        )
