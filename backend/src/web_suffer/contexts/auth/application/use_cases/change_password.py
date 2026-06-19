import structlog

from web_suffer.contexts.auth.application.dtos.user_dto import ChangePasswordDTO
from web_suffer.contexts.auth.application.exceptions import (
    InvalidAccessTokenError,
    InvalidCredentialsError,
)
from web_suffer.contexts.auth.application.interfaces import IPasswordHasher
from web_suffer.contexts.auth.application.interfaces.token_service import ITokenService
from web_suffer.contexts.auth.domain.repositories import IUserRepository
from web_suffer.contexts.auth.domain.value_objects import PasswordHash
from web_suffer.contexts.auth.domain.value_objects.token import Token

logger = structlog.stdlib.get_logger()


class ChangePasswordUseCase:
    """Use case смены пароля."""

    def __init__(
        self,
        user_repo: IUserRepository,
        token_service: ITokenService,
        password_hasher: IPasswordHasher,
    ) -> None:
        """Инициализирует use case смены пароля."""
        self._user_repo = user_repo
        self._token_service = token_service
        self._password_hasher = password_hasher

    async def execute(self, input_dto: ChangePasswordDTO) -> None:
        """
        Меняет пароль пользователя по access_token.

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

        password_hash = self._password_hasher.hash_password(password=input_dto.new_password)

        user.set_password_hash(PasswordHash(password_hash))

        await self._user_repo.save(user=user)
