import structlog

from web_suffer.contexts.auth.application.dtos.token_dto import (
    AccessTokenDTO,
)
from web_suffer.contexts.auth.application.dtos.user_dto import LoginDTO
from web_suffer.contexts.auth.application.exceptions import (
    InvalidAccessTokenError,
    InvalidCredentialsError,
)
from web_suffer.contexts.auth.application.interfaces.token_service import ITokenService
from web_suffer.contexts.auth.application.mappers.auth_dto_mapper import (
    IAuthDTOMapper,
)
from web_suffer.contexts.auth.domain.repositories import IUserRepository
from web_suffer.contexts.auth.domain.value_objects.token import Token

logger = structlog.stdlib.get_logger()


class GetLoginByAccessTokenUseCase:
    """Use case входа пользователя в аккаунт."""

    def __init__(
        self,
        user_repo: IUserRepository,
        token_service: ITokenService,
        mapper: IAuthDTOMapper,
    ) -> None:
        """Инициализирует use case входа пользователя в аккаунт."""
        self._user_repo = user_repo
        self._token_service = token_service
        self._mapper = mapper

    async def execute(self, input_dto: AccessTokenDTO) -> LoginDTO:
        """
        Возвращает логин пользователя по access_tocken.

        Returns:
            DTO с логином пользователя.

        Raises:
            InvalidAccessTokenError: неверный формат access token
            InvalidCredentialsError: нет пользователя с указанным ID

        """  # noqa: RUF002
        user_id = self._token_service.get_user_id_by_access_token(
            access_token=Token(input_dto.access_token),
        )
        if user_id is None:
            logger.warning("auth.email.failed", reason="token_not_valid")
            raise InvalidAccessTokenError

        logger.info("auth.email.succesed", id=str(user_id.value))

        user = await self._user_repo.get_user_by_id(
            user_id=user_id,
        )
        if user is None:
            logger.warning("auth.email.failed", reason="user_not_found")
            raise InvalidCredentialsError

        return self._mapper.to_login_dto(user)
