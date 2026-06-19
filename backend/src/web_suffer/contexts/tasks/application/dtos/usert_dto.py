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
    add_exp: int
    add_money: int
