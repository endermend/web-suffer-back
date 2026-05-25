from web_suffer.contexts.auth.application.dtos.token_dto import (
    AccessTokenDTO,
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
    UserRole,
    UserStatus,
)
from web_suffer.contexts.auth.domain.value_objects.token_pair import TokenPair


class AuthDTOMapper(IAuthDTOMapper):
    """Mapper между Domain Entity и DTO."""

    @staticmethod
    def to_user_dto(user: User) -> UserDTO:
        """
        Domain Entity -> DTO.

        Returns:
            Immutable User DTO.

        """
        return UserDTO(
            email=user.email.value,
            role=user.role.value,
            created_at=user.created_at,
            updated_at=user.updated_at,
            status=user.status.value,
        )

    @staticmethod
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
    def update_from_dto(
        user: User,
        update_dto: UpdateUserDTO,
    ) -> None:
        """Обновляет Domain Entity из DTO."""
        if update_dto.email is not None:
            user.set_email(UserEmail(update_dto.email))
        if update_dto.role is not None:
            user.set_role(UserRole(update_dto.role))
        if update_dto.status is not None:
            user.set_status(UserStatus(update_dto.status))

    @staticmethod
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
