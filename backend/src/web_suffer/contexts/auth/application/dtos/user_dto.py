from dataclasses import dataclass
from uuid import UUID

from web_suffer.contexts.auth.domain.types import UserRolesType, UserStatusType


@dataclass(slots=True, frozen=True)
class CredentialsDTO:
    """DTO логина с паролем."""  # noqa: RUF002

    email: str
    password: str


@dataclass(slots=True, frozen=True)
class LoginDTO:
    """DTO логина."""

    email: str


@dataclass(slots=True, frozen=True)
class UpdateUserDTO:
    """DTO для обновления пользователя."""

    access_token: str

    user_id: UUID | None = None
    email: str | None = None
    role: UserRolesType | None = None
    status: UserStatusType | None = None
    new_password: str | None = None


@dataclass(slots=True, frozen=True)
class UserDTO:
    """DTO пользователя."""

    user_id: UUID
    email: str
    role: UserRolesType
    status: UserStatusType


@dataclass(slots=True, frozen=True)
class GetUserDTO:
    """DTO получения данных пользователя."""

    access_token: str

    user_id: UUID | None = None
