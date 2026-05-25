import structlog

from web_suffer.contexts.auth.application.dtos.token_dto import TokensDTO
from web_suffer.contexts.auth.application.dtos.user_dto import CredentialsDTO
from web_suffer.contexts.auth.application.exceptions import InvalidCredentialsError
from web_suffer.contexts.auth.application.interfaces import (
    IPasswordHasher,
    ITokenService,
)
from web_suffer.contexts.auth.application.mappers.auth_dto_mapper import IAuthDTOMapper
from web_suffer.contexts.auth.domain.repositories import IUserRepository
from web_suffer.contexts.auth.domain.value_objects import UserEmail

logger = structlog.stdlib.get_logger()


class LoginUserUseCase:
    """Use case входа пользователя в аккаунт."""

    def __init__(
        self,
        user_repo: IUserRepository,
        password_hasher: IPasswordHasher,
        token_service: ITokenService,
        mapper: IAuthDTOMapper,
    ) -> None:
        """Инициализирует use case входа пользователя в аккаунт."""
        self._user_repo = user_repo
        self._password_hasher = password_hasher
        self._token_service = token_service
        self._mapper = mapper

    async def execute(self, input_dto: CredentialsDTO) -> TokensDTO:
        """
        Проверяет данные пользователя и возвращает пару токенов.

        Returns:
            DTO с парой токенов.

        Raises:
            InvalidCredentialsError: отсутствие пользователя с данной почтой
            InvalidCredentialsError: неверный пароль

        """  # noqa: RUF002
        user = await self._user_repo.get_user_by_email(email=UserEmail(input_dto.email))
        if user is None:
            logger.warning("auth.login.failed", reason="user_not_found")
            raise InvalidCredentialsError

        if not self._password_hasher.verify_password(
            password=input_dto.password,
            password_hash=user.password_hash,
        ):
            logger.warning(
                "auth.login.failed",
                reason="invalid_password",
                user_id=str(user.id.value),
            )
            raise InvalidCredentialsError

        token_pair = await self._token_service.create_token_pair(user_id=user.id)

        logger.info("auth.login.success", user_id=str(user.id.value))

        return TokensDTO(
            access_token=token_pair.access_token.value,
            refresh_token=token_pair.refresh_token.value,
        )
