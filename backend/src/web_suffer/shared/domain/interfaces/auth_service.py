from abc import ABC, abstractmethod

from web_suffer.shared.domain.value_objects.user_id import UserID


class IAuthService(ABC):
    """Сервис аутентификации для контекста задач."""

    @abstractmethod
    async def get_user_id_by_token(self, acess_token: str) -> UserID:
        """Получить ID пользователя по токену."""
