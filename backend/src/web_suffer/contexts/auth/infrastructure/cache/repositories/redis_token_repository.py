import json
from typing import TYPE_CHECKING, cast, override

from redis.asyncio.client import Redis

from web_suffer.contexts.auth.domain.repositories import ITokenRepository
from web_suffer.contexts.auth.domain.value_objects.token import Token
from web_suffer.shared.domain.value_objects import UserID

if TYPE_CHECKING:
    from collections.abc import Awaitable


class RedisTokenRepository(ITokenRepository):
    """Реализация ITokenRepository на Redis."""

    def __init__(self, redis: Redis) -> None:
        """Инициализация RedisTokenRepository."""
        self._redis = redis

    @override
    async def save_refresh_token(
        self,
        user_id: UserID,
        refresh_token: Token,
        ttl_seconds: int,
    ) -> None:
        """Сохранения refresh token."""
        token_data = json.dumps(
            {
                "user_id": str(user_id.value),
            },
        )

        async with self._redis.pipeline(transaction=True) as pipe:
            await pipe.setex(
                name=f"refresh:{refresh_token.value}",
                time=ttl_seconds,
                value=token_data,
            )
            await cast(
                "Awaitable[int]",
                pipe.sadd(f"refresh_sessions:{user_id.value}", refresh_token.value),
            )
            await pipe.execute()

    @override
    async def get_user_id_by_refresh_token(self, refresh_token: Token) -> UserID | None:
        """
        Получение UserID по значению refresh token.

        Returns:
            UserID | None: None если токен не найден или истёк.

        """
        value = await self._redis.get(name=f"refresh:{refresh_token.value}")
        value = cast("str | None", value)
        if value is None:
            return None

        data: dict[str, str] = json.loads(value)
        user_id_str = data["user_id"]
        return UserID.from_str(user_id_str)

    @override
    async def delete_refresh_token(
        self,
        refresh_token: Token,
    ) -> None:
        """Удаление refresh token."""
        user_id = await self.get_user_id_by_refresh_token(refresh_token=refresh_token)
        if user_id is None:
            return

        async with self._redis.pipeline(transaction=True) as pipe:
            await pipe.delete(f"refresh:{refresh_token.value}")
            await cast(
                "Awaitable[int]",
                pipe.srem(
                    f"refresh_sessions:{user_id.value}",
                    refresh_token.value,
                ),
            )
            await pipe.execute()
