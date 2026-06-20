from typing import override

from sqlalchemy import case, select
from sqlalchemy.ext.asyncio import AsyncSession

from web_suffer.contexts.auth.domain.entities import User
from web_suffer.contexts.auth.domain.repositories import IUserRepository
from web_suffer.contexts.auth.domain.value_objects import (
    UserEmail,
)
from web_suffer.contexts.auth.infrastructure.mappers.user_orm_mapper import (
    UserORMMapper,
)
from web_suffer.contexts.auth.infrastructure.persistence.models.user_model import (
    UserORMModel,
)
from web_suffer.shared.domain.value_objects import UserID


class UserRepository(IUserRepository):
    """Реализация IUserRepository на SQLAlchemy."""

    def __init__(self, session: AsyncSession, mapper: UserORMMapper) -> None:
        """Инициализация UserRepository."""
        self._session = session
        self._mapper = mapper

    @override
    async def save(self, user: User) -> None:
        """Сохранение User."""
        user_orm = UserORMModel()
        self._mapper.update_from_domain(orm=user_orm, user=user)
        await self._session.merge(user_orm)
        await self._session.commit()

    @override
    async def user_exists_by_email(self, email: UserEmail) -> bool:
        """
        Проверка существования User по UserEmail.

        Returns:
            bool: True если существует, False иначе

        """
        stmt = select(UserORMModel).where(UserORMModel.email == email.value)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None

    @override
    async def get_user_by_email(self, email: UserEmail) -> User | None:
        """
        Получение User по UserEmail.

        Returns:
            User | None: None если пользователь не найден.

        """
        stmt = select(UserORMModel).where(UserORMModel.email == email.value)
        result = await self._session.execute(stmt)
        user_orm = result.scalar()
        if user_orm is None:
            return None
        return self._mapper.to_domain(orm=user_orm)

    @override
    async def get_user_by_id(self, user_id: UserID) -> User | None:
        """
        Получение User по UserId.

        Returns:
            Пользователь, если пользователь с таким ID существует, иначе None.

        """  # noqa: RUF002
        user_orm = await self._session.get(UserORMModel, user_id.value)
        if user_orm is None:
            return None
        return self._mapper.to_domain(orm=user_orm)

    @override
    async def get_users(self) -> list[User]:
        """
        Получение списка User с ролью user.

        Returns:
            Список пользователей или пустой список.

        """  # noqa: RUF002
        stmt = select(UserORMModel)
        result = await self._session.execute(stmt)
        users_orm = result.scalars()
        return [self._mapper.to_domain(orm=user_orm) for user_orm in users_orm]

    @override
    async def get_users_by_id(self, users_id: list[UserID]) -> list[User]:
        """
        Получения списка User по списку id.

        Returns:
            Список пользователей.

        """
        if not users_id:
            return []

        ids_list = [user_id.value for user_id in users_id]

        order_by_case = case({id: index for index, id in enumerate(ids_list)}, value=UserORMModel.id)  # noqa: A001

        stmt = select(UserORMModel).where(UserORMModel.id.in_(ids_list)).order_by(order_by_case)

        result = await self._session.execute(stmt)
        users_orm = result.scalars()
        return [self._mapper.to_domain(orm=user_orm) for user_orm in users_orm]
