from dataclasses import dataclass
from datetime import datetime
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

    email: str
    role: str
    created_at: datetime
    updated_at: datetime
    status: int


@dataclass(slots=True, frozen=True)
class ChangePasswordDTO:
    """DTO смены пароля."""

    access_token: str
    new_password: str
