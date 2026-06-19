from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe
from typing import Any, override

import jwt
import structlog
from jwt.exceptions import InvalidTokenError

from web_suffer.contexts.auth.application.interfaces.token_service import ITokenService
from web_suffer.contexts.auth.domain.repositories import ITokenRepository
from web_suffer.contexts.auth.domain.value_objects.token import Token
from web_suffer.contexts.auth.domain.value_objects.token_pair import TokenPair
from web_suffer.infrastructure.config import JWT
from web_suffer.shared.domain.value_objects import UserID

logger = structlog.stdlib.get_logger()


class TokenService(ITokenService):
    """Реализация ITokenService."""

    def __init__(self, token_repository: ITokenRepository, jwt_config: JWT) -> None:
        """Инициализация TokenService."""
        self._token_repository = token_repository
        self._algorithm = jwt_config.ALGORITHM
        self._secret_key = jwt_config.SECRET_KEY
        self._access_exp = jwt_config.ACCESS_EXPIRE_SECONDS
        self._refresh_exp = jwt_config.REFRESH_EXPIRE_SECONDS

    @override
    async def create_token_pair(self, user_id: UserID) -> TokenPair:
        """
        Создание пары токенов.

        Returns:
            TokenPair

        """
        now = datetime.now(UTC)
        payload: dict[str, Any] = {
            "sub": str(user_id.value),
            "iat": now,
            "exp": now + timedelta(seconds=self._access_exp),
        }
        access_token = jwt.encode(
            payload=payload,
            key=self._secret_key,
            algorithm=self._algorithm,
        )

        refresh_token = token_urlsafe(32)

        await self._token_repository.save_refresh_token(
            user_id=user_id,
            refresh_token=Token(refresh_token),
            ttl_seconds=self._refresh_exp,
        )

        return TokenPair(
            access_token=Token(access_token),
            refresh_token=Token(refresh_token),
        )

    @override
    async def get_user_id_by_refresh_token(self, refresh_token: Token) -> UserID | None:
        """
        Получение UserID по значению refresh_token.

        Returns:
            UserID | None:  None если токен не найден или истёк

        """
        return await self._token_repository.get_user_id_by_refresh_token(
            refresh_token=refresh_token,
        )

    @override
    def get_user_id_by_access_token(self, access_token: Token) -> UserID | None:
        """
        Получение UserID по значению access_token.

        Returns:
            UserID | None:  None если токен не найден

        """
        try:
            payload = jwt.decode(
                jwt=access_token.value,
                key=self._secret_key,
                algorithms=[self._algorithm],
            )
        except InvalidTokenError:
            return None
        return UserID.from_str(payload["sub"])

    @override
    async def revoke_refresh_token(self, refresh_token: Token) -> None:
        """Отзыв refresh token."""
        await self._token_repository.delete_refresh_token(refresh_token=refresh_token)
