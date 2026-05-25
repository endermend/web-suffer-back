import structlog

from web_suffer.contexts.auth.application.dtos.token_dto import TokensDTO
from web_suffer.contexts.auth.application.dtos.user_dto import CredentialsDTO
from web_suffer.contexts.auth.application.exceptions import EmailAlreadyExistsError
from web_suffer.contexts.auth.application.interfaces.password_hasher import (
    IPasswordHasher,
)
from web_suffer.contexts.auth.application.interfaces.token_service import ITokenService
from web_suffer.contexts.auth.application.mappers.auth_dto_mapper import IAuthDTOMapper
from web_suffer.contexts.auth.domain.repositories import IUserRepository
from web_suffer.contexts.auth.domain.value_objects import (
    UserEmail,
)

logger = structlog.stdlib.get_logger()


class RegisterUserUseCase:
    """Use case регистрации пользователя."""

    def __init__(
        self,
        user_repo: IUserRepository,
        password_hasher: IPasswordHasher,
        token_service: ITokenService,
        mapper: IAuthDTOMapper,
    ) -> None:
        """Инициализирует UseCase регистрации пользователя."""
        self._user_repo = user_repo
        self._password_hasher = password_hasher
        self._token_service = token_service
        self._mapper = mapper

    async def execute(self, input_dto: CredentialsDTO) -> TokensDTO:
        """
        Регистрирует нового пользователя и возвращает пару токенов.

        Returns:
            DTO с парой токенов.

        Raises:
            EmailAlreadyExistsError: пользователь с данным email уже существует.

        """  # noqa: RUF002
        user = await self._user_repo.get_user_by_email(email=UserEmail(input_dto.email))
        if user is not None:
            logger.warning(
                "auth.register.failed",
                reason="email_already_exists",
                user_id=str(user.id.value),
            )
            raise EmailAlreadyExistsError

        password_hash = self._password_hasher.hash_password(password=input_dto.password)
        user = self._mapper.create_from_dto(
            CredentialsDTO(
                email=input_dto.email,
                password=password_hash,
            ),
        )

        await self._user_repo.save(user=user)

        token_pair = await self._token_service.create_token_pair(user_id=user.id)

        logger.info("auth.register.success", user_id=str(user.id.value))

        return self._mapper.to_token_dto(
            token_pair=token_pair,
        )
