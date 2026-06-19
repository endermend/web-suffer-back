from abc import ABC, abstractmethod

from web_suffer.shared.domain.value_objects.user_id import UserID
from web_suffer.shared.domain.value_objects.user_right import UserRight


class IAuthService(ABC):
    """Сервис аутентификации для контекста задач."""

    @abstractmethod
    async def get_user_id_by_token(self, acess_token: str) -> UserID:
        """Получить ID пользователя по токену."""

    @abstractmethod
    async def check_user_right(self, user_id: UserID, right: UserRight) -> bool:
        """Проверка прав пользователя по ID."""
