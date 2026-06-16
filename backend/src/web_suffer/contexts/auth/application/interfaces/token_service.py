from typing import Protocol

from web_suffer.contexts.auth.domain.value_objects.token import Token
from web_suffer.contexts.auth.domain.value_objects.token_pair import TokenPair
from web_suffer.shared.domain.value_objects import UserID


class ITokenService(Protocol):
    """Сервис работы с токенами access и refresh."""  # noqa: RUF002

    async def create_token_pair(self, user_id: UserID) -> TokenPair:
        """Создание пары токенов."""

    async def get_user_id_by_refresh_token(self, refresh_token: Token) -> UserID | None:
        """
        Получение UserID по значению refresh_token.

        None если токен не найден или истёк.
        """

    def get_user_id_by_access_token(self, access_token: Token) -> UserID | None:
        """
        Получение UserID по значению access_token.

        Returns:
            UserID | None:  None если токен не найден

        """

    async def revoke_refresh_token(self, refresh_token: Token) -> None:
        """Отзыв refresh token."""
