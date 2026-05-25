from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


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

    user_id: UUID
    email: str | None = None
    role: str | None = None
    status: int | None = None


@dataclass(slots=True, frozen=True)
class UserDTO:
    """DTO пользователя."""

    email: str
    role: str
    created_at: datetime
    updated_at: datetime
    status: int
