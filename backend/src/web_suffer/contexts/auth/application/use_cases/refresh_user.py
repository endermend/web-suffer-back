import structlog

from web_suffer.contexts.auth.application.dtos.token_dto import (
    RefreshTokenDTO,
    TokensDTO,
)
from web_suffer.contexts.auth.application.exceptions import InvalidRefreshTokenError
from web_suffer.contexts.auth.application.interfaces import ITokenService
from web_suffer.contexts.auth.application.mappers.auth_dto_mapper import IAuthDTOMapper
from web_suffer.contexts.auth.domain.value_objects.token import Token

logger = structlog.stdlib.get_logger()


class RefreshUserUseCase:
    """Use case обновления токенов пользователя."""

    def __init__(
            self,
            token_service: ITokenService,
            mapper: IAuthDTOMapper,
        ) -> None:
        """Инициализирует use case обновления токенов пользователя."""
        self._token_service = token_service
        self._mapper = mapper

    async def execute(self, input_dto: RefreshTokenDTO) -> TokensDTO:
        """
        Принимает старый refresh token и возвращает новую пару токенов.

        Returns:
            DTO с парой токенов.

        Raises:
            InvalidRefreshTokenError: токен не найден в redis.

        """  # noqa: RUF002
        user_id = await self._token_service.get_user_id_by_refresh_token(
            refresh_token=Token(input_dto.refresh_token),
        )
        if user_id is None:
            logger.warning(
                "auth.refresh.failed",
                reason="invalid_token",
            )
            raise InvalidRefreshTokenError

        await self._token_service.revoke_refresh_token(
            refresh_token=Token(input_dto.refresh_token),
        )

        token_pair = await self._token_service.create_token_pair(user_id=user_id)

        logger.info("auth.refresh.success", user_id=str(user_id.value))

        return self._mapper.to_token_dto(
            token_pair=token_pair,
        )
