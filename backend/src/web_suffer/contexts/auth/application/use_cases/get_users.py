import structlog

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
from web_suffer.shared.application.dtos.access_token_dto import AccessTokenDTO
from web_suffer.shared.application.dtos.user_id_dto import UserIDDTO
from web_suffer.shared.domain.exceptions import InsufficientPermissionsError
from web_suffer.shared.domain.value_objects.user_rights import UserRights

logger = structlog.stdlib.get_logger()


class GetUsersUseCase:
    """Use case получения списка пользователей для админа."""

    def __init__(
        self,
        user_repo: IUserRepository,
        token_service: ITokenService,
        mapper: IAuthDTOMapper,
    ) -> None:
        """Инициализирует use case получения списка пользователей для админа."""
        self._user_repo = user_repo
        self._token_service = token_service
        self._mapper = mapper

    async def execute(self, input_dto: AccessTokenDTO) -> list[UserIDDTO]:
        """
        Возвращает список почт пользователей.

        Returns:
            list[UserIDDTO]: список пользователей

        Raises:
            InvalidAccessTokenError: неверный формат access token
            InvalidCredentialsError: нет пользователя с указанным ID
            InsufficientPermissionsError: у пользователя недостаточно прав.

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

        if not UserRights.CHECK_USER_LIST.is_satisfied_by(user.role, user.status):
            logger.warning("auth.email.failed", reason="not_enought_permission")
            raise InsufficientPermissionsError

        users = await self._user_repo.get_users()

        return [self._mapper.to_userid_dto(user_id=user.id) for user in users]
