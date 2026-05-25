from typing import ClassVar

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
        return self.value == 0


UserStatus.ACTIVE = UserStatus(0)
UserStatus.BANNED = UserStatus(1)
UserStatus.DELETED = UserStatus(2)
