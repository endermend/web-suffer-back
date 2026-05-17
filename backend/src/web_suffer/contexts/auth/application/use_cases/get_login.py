import structlog

from web_suffer.contexts.auth.application.dto.get_login import (
    GetLoginInputDTO,
    GetLoginOutputDTO,
)
from web_suffer.contexts.auth.application.exceptions import (
    InvalidAccessTokenError,
    InvalidCredentialsError,
)
from web_suffer.contexts.auth.domain.repositories import IUserRepository
from web_suffer.contexts.auth.domain.security import ITokenService

logger = structlog.stdlib.get_logger()


class GetLoginUseCase:
    """Use case входа пользователя в аккаунт."""

    def __init__(
        self,
        user_repo: IUserRepository,
        token_service: ITokenService,
    ) -> None:
        """Инициализирует use case входа пользователя в аккаунт."""
        self._user_repo = user_repo
        self._token_service = token_service

    async def execute(self, input_dto: GetLoginInputDTO) -> GetLoginOutputDTO:
        """
        Возвращает логин пользователя по access_tocken.

        Returns:
            DTO с парой токенов.

        Raises:
            InvalidAccessTokenError: неверный формат access token
            InvalidCredentialsError: нет пользователя с указанным ID

        """  # noqa: RUF002
        user_id = self._token_service.get_user_id_by_access_token(
            access_token=input_dto.access_token,
        )
        if user_id is None:
            logger.warning("auth.email.failed", reason="token_not_valid")
            raise InvalidAccessTokenError

        user = await self._user_repo.get_user_by_id(
            user_id=user_id,
        )
        if user is None:
            logger.warning("auth.email.failed", reason="user_not_found")
            raise InvalidCredentialsError

        email = user.email.value

        return GetLoginOutputDTO(
            email=email,
        )
