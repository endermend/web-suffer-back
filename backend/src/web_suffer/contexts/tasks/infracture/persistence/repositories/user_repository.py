from web_suffer.contexts.tasks.domain.entities.user import UserT
from web_suffer.contexts.tasks.domain.repository.user_repository import IUserTRepository
from web_suffer.shared.domain.value_objects.user_id import UserID


class UserTRepository(IUserTRepository):
    """Протокол UserT репозитория."""

    async def save(self, user: UserT) -> None:
        """Сохранение UserT."""

    async def get_user_by_id(self, task_id: UserID) -> UserT | None:
        """
        Получение UserT по UserID.

        None, если user не найден.
        """

    async def change_user(self, user: UserT) -> None:
        """Обновление параметров UserT."""
