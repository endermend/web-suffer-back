from typing import override

from web_suffer.contexts.auth.application.dtos.token_dto import (
    RefreshTokenDTO,
    TokensDTO,
)
from web_suffer.contexts.auth.application.dtos.user_dto import (
    CredentialsDTO,
    LoginDTO,
    UpdateUserDTO,
    UserDTO,
)
from web_suffer.contexts.auth.application.mappers.auth_dto_mapper import IAuthDTOMapper
from web_suffer.contexts.auth.domain.entities.user import User
from web_suffer.contexts.auth.domain.value_objects import (
    PasswordHash,
    UserEmail,
)
from web_suffer.contexts.auth.domain.value_objects.token_pair import TokenPair
from web_suffer.shared.application.dtos.access_token_dto import AccessTokenDTO
from web_suffer.shared.application.dtos.user_id_dto import UserIDDTO
from web_suffer.shared.domain.value_objects.user_id import UserID
from web_suffer.shared.domain.value_objects.user_role import UserRole
from web_suffer.shared.domain.value_objects.user_status import UserStatus


class AuthDTOMapper(IAuthDTOMapper):
    """Mapper между Domain Entity и DTO."""

    @staticmethod
    @override
    def to_user_dto(user: User) -> UserDTO:
        """
        Domain Entity -> DTO.

        Returns:
            Immutable User DTO.

        """
        return UserDTO(
            user_id=user.id.value,
            email=user.email.value,
            role=user.role.to_str(),
            status=user.status.to_str(),
        )

    @staticmethod
    @override
    def to_login_dto(user: User) -> LoginDTO:
        """
        Domain Entity -> Login DTO.

        Returns:
            Immutable Login DTO.

        """
        return LoginDTO(
            email=user.email.value,
        )

    @staticmethod
    @override
    def create_from_dto(
        create_dto: CredentialsDTO,
    ) -> User:
        """
        CreateUserDTO -> Domain Entity.

        Returns:
            New User.

        """
        return User.register(
            UserEmail(create_dto.email),
            PasswordHash(create_dto.password),
            UserRole.USER,
        )

    @staticmethod
    @override
    def update_from_dto(
        user: User,
        update_dto: UpdateUserDTO,
    ) -> None:
        """Обновляет Domain Entity из DTO."""
        if update_dto.email is not None:
            user.set_email(UserEmail(update_dto.email))
        if update_dto.role is not None:
            user_role = UserRole.from_str(user_role_str=update_dto.role)
            user.set_role(user_role)
        if update_dto.status is not None:
            user_status = UserStatus.from_str(user_status_str=update_dto.status)
            user.set_status(user_status)

    @staticmethod
    @override
    def to_access_dto(
        token_pair: TokenPair,
    ) -> AccessTokenDTO:
        """
        Domain Entity -> DTO.

        Returns:
            Immutable Access DTO.

        """
        return AccessTokenDTO(
            access_token=token_pair.access_token.value,
        )

    @staticmethod
    @override
    def to_refresh_dto(
        token_pair: TokenPair,
    ) -> RefreshTokenDTO:
        """
        Domain Entity -> DTO.

        Returns:
            Immutable Refresh DTO.

        """
        return RefreshTokenDTO(
            refresh_token=token_pair.refresh_token.value,
        )

    @staticmethod
    @override
    def to_token_dto(
        token_pair: TokenPair,
    ) -> TokensDTO:
        """
        Domain Entity -> DTO.

        Returns:
            Immutable Token DTO.

        """
        return TokensDTO(
            access_token=token_pair.access_token.value,
            refresh_token=token_pair.refresh_token.value,
        )

    @staticmethod
    @override
    def from_userid_dto(
        user_id: UserIDDTO,
    ) -> UserID:
        """
        DTO -> Domain Entity.

        Returns:
            Immutable UserID DTO.

        """
        return UserID(value=user_id.user_id)

    @staticmethod
    @override
    def to_userid_dto(
        user_id: UserID,
    ) -> UserIDDTO:
        """
        Domain Entity -> DTO.

        Returns:
            Immutable UserID DTO.

        """
        return UserIDDTO(user_id=user_id.value)
