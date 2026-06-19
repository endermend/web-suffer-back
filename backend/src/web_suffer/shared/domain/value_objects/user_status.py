from typing import ClassVar

from web_suffer.contexts.auth.domain.types import UserStatusType
from web_suffer.shared.domain.exceptions import DomainError
from web_suffer.shared.domain.value_objects.single_value_object import SingleValueObject


class UserStatus(SingleValueObject):
    """Value object статуса пользователя."""

    value: int

    ACTIVE: ClassVar["UserStatus"]
    BANNED: ClassVar["UserStatus"]
    DELETED: ClassVar["UserStatus"]

    def is_active(self) -> bool:
        """
        Активен ли пользователь.

        Returns:
            True, если пользователь активен.

        """
        return self.value == UserStatus.ACTIVE.value

    @staticmethod
    def from_str(user_status_str: UserStatusType) -> "UserStatus":
        """
        Преобразует строку в UserStatus.

        Returns:
            UserStatus

        Raises:
            DomainError: если не смог преобразовать

        """
        if user_status_str == "active":
            return UserStatus.ACTIVE
        if user_status_str == "banned":
            return UserStatus.BANNED
        if user_status_str == "deleted":
            return UserStatus.DELETED
        raise DomainError  # FIXME: изменить на более подходящую  # noqa: FIX001, TD001

    def to_str(self) -> UserStatusType:
        """
        Преобразует в строку.

        Returns:
            UserStatusType

        Raises:
            DomainError: если не смог преобразовать

        """
        if self.value == UserStatus.ACTIVE.value:
            return "active"
        if self.value == UserStatus.BANNED.value:
            return "banned"
        if self.value == UserStatus.DELETED.value:
            return "deleted"
        raise DomainError  # FIXME: изменить на более подходящую  # noqa: FIX001, TD001


UserStatus.ACTIVE = UserStatus(0)
UserStatus.BANNED = UserStatus(1)
UserStatus.DELETED = UserStatus(2)
