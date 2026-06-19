import structlog

from web_suffer.contexts.auth.application.dtos.user_dto import GetUserDTO, UserDTO
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
from web_suffer.shared.domain.exceptions import DomainError, InsufficientPermissionsError
from web_suffer.shared.domain.value_objects import UserID
from web_suffer.shared.domain.value_objects.user_rights import UserRights

logger = structlog.stdlib.get_logger()


class GetUserByUserIDUseCase:
    """Use case получения логина по access-токену."""

    def __init__(
        self,
        user_repo: IUserRepository,
        token_service: ITokenService,
        mapper: IAuthDTOMapper,
    ) -> None:
        """Инициализирует use case получения логина по access-токену."""
        self._user_repo = user_repo
        self._token_service = token_service
        self._mapper = mapper

    async def execute(self, input_dto: GetUserDTO) -> UserDTO:
        """
        Возвращает данные пользователя.

        Returns:
            DTO с данными пользователя.

        Raises:
            InvalidAccessTokenError: неверный формат access token
            InvalidCredentialsError: нет пользователя с указанным ID
            DomainError: нет пользователя с указанным ID
            InsufficientPermissionsError: нет прав

        """  # noqa: RUF002
        user_id = self._token_service.get_user_id_by_access_token(
            access_token=Token(input_dto.access_token),
        )
        if user_id is None:
            logger.warning("auth.get_user.failed", reason="token_not_valid")
            raise InvalidAccessTokenError

        logger.info("auth.get_user.succesed", id=str(user_id.value))

        user = await self._user_repo.get_user_by_id(
            user_id=user_id,
        )
        if user is None:
            logger.warning("auth.get_user.failed", reason="user_not_found")
            raise InvalidCredentialsError

        # Пользователь смотрит себя
        if input_dto.user_id is None or (input_dto.user_id is not None and input_dto.user_id == user_id.value):
            logger.info("auth.get_user.succesed.self")
            return self._mapper.to_user_dto(user=user)

        # Админ/модер смотрит пользователя
        if input_dto.user_id is not None and UserRights.VIEW_USER.is_satisfied_by(role=user.role, status=user.status):
            user = await self._user_repo.get_user_by_id(user_id=UserID(input_dto.user_id))
            if user is None:
                logger.warning("auth.get_user.failed", reason="user_not_found")
                raise DomainError
            logger.info("auth.get_user.succesed.other")
            return self._mapper.to_user_dto(user=user)

        error = "Not enough permission."
        logger.warning("auth.get_user.failed", reason="not_enough_permission")
        raise InsufficientPermissionsError(error)
