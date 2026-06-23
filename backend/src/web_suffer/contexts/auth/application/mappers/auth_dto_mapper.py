from abc import abstractmethod
from typing import Protocol

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
from web_suffer.contexts.auth.domain.entities.user import User
from web_suffer.contexts.auth.domain.value_objects.token_pair import TokenPair
from web_suffer.shared.application.dtos.access_token_dto import AccessTokenDTO
from web_suffer.shared.application.dtos.user_id_dto import UserIDDTO
from web_suffer.shared.domain.value_objects.user_id import UserID


class IAuthDTOMapper(Protocol):
    """Mapper между Domain Entity и DTO."""

    @staticmethod
    @abstractmethod
    def to_user_dto(user: User) -> UserDTO:
        """
        Domain Entity -> DTO.

        Returns:
            Immutable User DTO.

        """

    @staticmethod
    @abstractmethod
    def to_login_dto(user: User) -> LoginDTO:
        """
        Domain Entity -> Login DTO.

        Returns:
            Immutable Login DTO.

        """

    @staticmethod
    @abstractmethod
    def create_from_dto(
        create_dto: CredentialsDTO,
    ) -> User:
        """
        CreateUserDTO -> Domain Entity.

        Returns:
            New User.

        """

    @staticmethod
    @abstractmethod
    def update_from_dto(
        user: User,
        update_dto: UpdateUserDTO,
    ) -> None:
        """Обновляет Domain Entity из DTO."""

    @staticmethod
    @abstractmethod
    def to_access_dto(
        token_pair: TokenPair,
    ) -> AccessTokenDTO:
        """
        Domain value object -> DTO.

        Returns:
            Immutable Access DTO.

        """

    @staticmethod
    @abstractmethod
    def to_refresh_dto(
        token_pair: TokenPair,
    ) -> RefreshTokenDTO:
        """
        Domain value object -> DTO.

        Returns:
            Immutable Refresh DTO.

        """

    @staticmethod
    @abstractmethod
    def to_token_dto(
        token_pair: TokenPair,
    ) -> TokensDTO:
        """
        Domain value object -> DTO.

        Returns:
            Immutable Token DTO.

        """

    @staticmethod
    @abstractmethod
    def from_userid_dto(
        user_id: UserIDDTO,
    ) -> UserID:
        """
        DTO -> Domain value object, based on DTO.

        Returns:
            Domain UserID value object.

        """

    @staticmethod
    @abstractmethod
    def to_userid_dto(
        user_id: UserID,
    ) -> UserIDDTO:
        """
        Domain value object -> DTO.

        Returns:
            Immutable UserID DTO.

        """
