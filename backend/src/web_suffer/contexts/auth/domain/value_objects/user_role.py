
from typing import ClassVar

from web_suffer.shared.domain.value_objects.single_value_object import SingleValueObject


class UserRole(SingleValueObject):
    """Value object роли пользователя."""

    value: str

    USER: ClassVar["UserRole"]
    ADMIN: ClassVar["UserRole"]
    MODERATOR: ClassVar["UserRole"]


UserRole.USER = UserRole("user")
UserRole.ADMIN = UserRole("admin")
UserRole.MODERATOR = UserRole("moderator")
