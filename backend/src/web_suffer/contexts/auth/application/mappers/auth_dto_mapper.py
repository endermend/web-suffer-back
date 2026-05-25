from typing import Protocol

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
from web_suffer.contexts.auth.domain.entities.user import User
from web_suffer.contexts.auth.domain.value_objects.token_pair import TokenPair


class IAuthDTOMapper(Protocol):
    """Mapper между Domain Entity и DTO."""

    @staticmethod
    def to_user_dto(user: User) -> UserDTO:
        """
        Domain Entity -> DTO.

        Returns:
            Immutable User DTO.

        """

    @staticmethod
    def to_login_dto(user: User) -> LoginDTO:
        """
        Domain Entity -> Login DTO.

        Returns:
            Immutable Login DTO.

        """

    @staticmethod
    def create_from_dto(
        create_dto: CredentialsDTO,
    ) -> User:
        """
        CreateUserDTO -> Domain Entity.

        Returns:
            New User.

        """

    @staticmethod
    def update_from_dto(
        user: User,
        update_dto: UpdateUserDTO,
    ) -> None:
        """Обновляет Domain Entity из DTO."""

    @staticmethod
    def to_access_dto(
        token_pair: TokenPair,
    ) -> AccessTokenDTO:
        """
        Domain Entity -> DTO.

        Returns:
            Immutable Access DTO.

        """

    @staticmethod
    def to_refresh_dto(
        token_pair: TokenPair,
    ) -> RefreshTokenDTO:
        """
        Domain Entity -> DTO.

        Returns:
            Immutable Refresh DTO.

        """

    @staticmethod
    def to_token_dto(
        token_pair: TokenPair,
    ) -> TokensDTO:
        """
        Domain Entity -> DTO.

        Returns:
            Immutable Token DTO.

        """
