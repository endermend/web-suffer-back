from typing import Literal, override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from web_suffer.contexts.tasks.domain.entities.user import UserT
from web_suffer.contexts.tasks.domain.repository.user_repository import IUserTRepository
from web_suffer.contexts.tasks.infrastructure.mappers.usert_orm_mapper import UserTORMMapper
from web_suffer.contexts.tasks.infrastructure.persistence.models.user_model import UserTORMModel
from web_suffer.shared.domain.value_objects.user_id import UserID


class UserTRepository(IUserTRepository):
    """Протокол UserT репозитория."""

    def __init__(self, session: AsyncSession, mapper: UserTORMMapper) -> None:
        """Инициализация UserTRepository."""
        self._session = session
        self._mapper = mapper

    @override
    async def save(self, user: UserT) -> None:
        """Сохранение UserT."""
        async with self._session.begin():
            user_orm = await self._session.get(UserTORMModel, user.id.value)

            if not user_orm:
                user_orm = UserTORMModel()

            self._mapper.update_from_domain(orm=user_orm, user=user)
            self._session.add(user_orm)

    @override
    async def get_by_id(self, user_id: UserID) -> UserT | None:
        """
        Получение UserT по UserID.

        None, если user не найден.

        Returns:
            Пользователь по id.

        """
        user_orm = await self._session.get(UserTORMModel, user_id.value)
        if not user_orm:
            return None
        return self._mapper.to_domain(orm=user_orm)

    @override
    async def get_list(self, amount: int = 5, order_by: Literal["exp", "money"] = "exp") -> list[UserT]:
        """
        Получение UserT's.

        Returns:
            Список пользователей.

        """
        stmt = select(UserTORMModel)
        if order_by == "exp":
            stmt = stmt.order_by(UserTORMModel.exp)
        elif order_by == "money":
            stmt = stmt.order_by(UserTORMModel.money)

        stmt = stmt.limit(amount)
        result = await self._session.execute(stmt)
        users_orm = result.scalars()
        return [self._mapper.to_domain(orm=user_orm) for user_orm in users_orm]
