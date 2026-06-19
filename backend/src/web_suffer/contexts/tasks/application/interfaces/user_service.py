from typing import Protocol

from web_suffer.shared.domain.value_objects.user_id import UserID


class IUserService(Protocol):
    """Реализация IUserService."""

    async def update_user_by_id(self, user_id: UserID, exp_diff: int, money_diff: int) -> None:
        """Обновление пользователя по id."""
