import structlog

from web_suffer.contexts.auth.application.dtos.user_dto import UpdateUserDTO
from web_suffer.contexts.auth.application.exceptions import (
    EmailAlreadyExistsError,
    InvalidAccessTokenError,
    InvalidCredentialsError,
)
from web_suffer.contexts.auth.application.interfaces import IPasswordHasher
from web_suffer.contexts.auth.application.interfaces.token_service import ITokenService
from web_suffer.contexts.auth.application.mappers.auth_dto_mapper import IAuthDTOMapper
from web_suffer.contexts.auth.domain.repositories import IUserRepository
from web_suffer.contexts.auth.domain.value_objects import PasswordHash, UserEmail
from web_suffer.contexts.auth.domain.value_objects.token import Token
from web_suffer.shared.domain.exceptions import InsufficientPermissionsError
from web_suffer.shared.domain.value_objects.user_id import UserID
from web_suffer.shared.domain.value_objects.user_rights import UserRights
from web_suffer.shared.domain.value_objects.user_status import UserStatus

logger = structlog.stdlib.get_logger()


class UpdateUserUseCase:
    """Use case обновления данных пользователя."""

    def __init__(
        self,
        user_repo: IUserRepository,
        token_service: ITokenService,
        password_hasher: IPasswordHasher,
        mapper: IAuthDTOMapper,
    ) -> None:
        """Инициализирует use case обновления данных пользователя."""
        self._user_repo = user_repo
        self._token_service = token_service
        self._password_hasher = password_hasher
        self._mapper = mapper

    async def execute(self, input_dto: UpdateUserDTO) -> None:  # noqa: C901, PLR0912
        """
        Меняет пароль пользователя по access_token.

        Raises:
            InvalidAccessTokenError: неверный формат access token
            InvalidCredentialsError: нет пользователя с указанным ID
            InsufficientPermissionsError: у пользователя нет прав менять пользователя
            ValueError: пользователя с указанным ID не существует
            EmailAlreadyExistsError: попытка изменить почту на почту другого пользователя

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

        change_user = user
        no_user_id = input_dto.user_id is None
        change_self = (no_user_id or input_dto.user_id == user.id.value) and UserRights.CHANGE_SELF.is_satisfied_by(
            role=user.role,
            status=user.status,
        )
        change_other = not no_user_id and input_dto.user_id != user.id.value and UserRights.CHANGE_USER.is_satisfied_by(role=user.role, status=user.status)

        if not change_self and not change_other:
            raise InsufficientPermissionsError

        if change_other:
            input_user = await self._user_repo.get_user_by_id(
                user_id=UserID(input_dto.user_id),
            )

            if input_user is None:
                raise ValueError
            change_user = input_user

            if (input_dto.status is not None or input_dto.role is not None) and not UserRights.CHANGE_RESTRICTED_USER.is_satisfied_by(
                role=user.role,
                status=user.status,
            ):
                raise InsufficientPermissionsError

        elif change_self:
            if input_dto.role is not None:
                raise InsufficientPermissionsError
            if input_dto.status is not None:
                status = UserStatus.from_str(input_dto.status)
                if (status == UserStatus.DELETED and not UserRights.DELETE_ACCOUNT.is_satisfied_by(
                    role=user.role,
                    status=user.status,
                )) or (status == UserStatus.ACTIVE and not UserRights.RESTORE_ACCOUNT.is_satisfied_by(
                    role=user.role,
                    status=user.status,
                )) or status == UserStatus.BANNED:
                    raise InsufficientPermissionsError

        if input_dto.email is not None:
            user_email = await self._user_repo.get_user_by_email(email=UserEmail(input_dto.email))
            if user_email is not None and user_email != change_user:
                raise EmailAlreadyExistsError

        if input_dto.new_password:
            password_hash = self._password_hasher.hash_password(password=input_dto.new_password)
            change_user.set_password_hash(PasswordHash(password_hash))

        self._mapper.update_from_dto(user=change_user, update_dto=input_dto)

        await self._user_repo.save(user=change_user)
