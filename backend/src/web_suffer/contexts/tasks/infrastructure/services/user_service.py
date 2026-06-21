from typing import override

import structlog

from web_suffer.contexts.tasks.application.interfaces.user_service import IUserService
from web_suffer.contexts.tasks.domain.entities.user import UserT
from web_suffer.contexts.tasks.domain.repository.user_repository import IUserTRepository
from web_suffer.shared.domain.value_objects.user_id import UserID

logger = structlog.stdlib.get_logger()


class UserService(IUserService):
    """Реализация IUserService."""

    def __init__(self, user_repository: IUserTRepository) -> None:
        """Инициализация UserService."""
        self._user_repository = user_repository

    @override
    async def update_user_by_id(self, user_id: UserID, exp_diff: int, money_diff: int) -> None:
        """Обновление пользователя по id."""
        user = await self._user_repository.get_by_id(user_id)
        if user is None:
            user = UserT.create(id=user_id)

        user.add_exp(exp_diff)
        user.add_money(money_diff)

        await self._user_repository.save(user)
