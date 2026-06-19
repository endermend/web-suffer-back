from typing import Literal, Protocol

from web_suffer.contexts.tasks.domain.entities.user import UserT
from web_suffer.shared.domain.value_objects.user_id import UserID


class IUserTRepository(Protocol):
    """Протокол UserT репозитория."""

    async def save(self, user: UserT) -> None:
        """Сохранение UserT."""

    async def get_by_id(self, user_id: UserID) -> UserT | None:
        """
        Получение UserT по UserID.

        None, если user не найден.
        """

    async def get_list(self, amount: int = 5, order_by: Literal["exp", "money"] = "exp") -> list[UserT]:
        """
        Получение UserT's.

        Returns:
            Список пользователей.

        """
