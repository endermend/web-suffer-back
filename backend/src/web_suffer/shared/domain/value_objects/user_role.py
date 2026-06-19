from typing import ClassVar

from web_suffer.contexts.auth.domain.types import UserRolesType
from web_suffer.shared.domain.exceptions import DomainError
from web_suffer.shared.domain.value_objects.single_value_object import SingleValueObject


class UserRole(SingleValueObject):
    """Value object роли пользователя."""

    value: str

    USER: ClassVar["UserRole"]
    ADMIN: ClassVar["UserRole"]
    MODERATOR: ClassVar["UserRole"]

    @staticmethod
    def from_str(user_role_str: UserRolesType) -> "UserRole":
        """
        Преобразует строку в UserRole.

        Returns:
            UserRole

        Raises:
            DomainError: если не смог преобразовать

        """
        match user_role_str:
            case "user":
                return UserRole.USER
            case "admin":
                return UserRole.ADMIN
            case "moderator":
                return UserRole.MODERATOR
            case _:
                raise DomainError  # FIXME: изменить на более подходящую  # noqa: FIX001, TD001


UserRole.USER = UserRole("user")
UserRole.ADMIN = UserRole("admin")
UserRole.MODERATOR = UserRole("moderator")
