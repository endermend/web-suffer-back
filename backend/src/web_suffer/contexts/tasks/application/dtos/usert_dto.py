from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, frozen=True)
class UserTDTO:
    """DTO пользователя."""

    user_id: UUID
    exp: int
    money: int


@dataclass(slots=True, frozen=True)
class UpdateUserTDTO:
    """DTO обновления пользователя."""

    access_token: str
    user_id: UUID
    exp_diff: int
    money_diff: int


@dataclass(slots=True, frozen=True)
class UserTIDDTO:
    """DTO ID пользователя."""

    access_token: str
    user_id: UUID | None


@dataclass(slots=True, frozen=True)
class UserTTOPDTO:
    """DTO входных данных получения топа пользователей."""

    amount: int
