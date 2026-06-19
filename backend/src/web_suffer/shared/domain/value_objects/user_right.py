from dataclasses import dataclass
from typing import Any, ClassVar, Final, Literal

from web_suffer.shared.domain.value_objects.base_value_object import BaseValueObject
from web_suffer.shared.domain.value_objects.user_role import UserRole
from web_suffer.shared.domain.value_objects.user_status import UserStatus


@dataclass(slots=True, frozen=True)
class UserRight(BaseValueObject):
    """Право пользователей."""

    ALL: ClassVar[Literal["*"]] = "*"

    roles: set[UserRole] | Literal["*"]
    statuses: set[UserStatus] | Literal["*"]

    def __post_init__(self) -> None:
        """
        Проверка валидности права пользователя.

        Raises:
            ValueError: Если права невалидны.

        """
        roles_valid = self.roles == "*" or len(self.roles) > 0
        statuses_valid = self.statuses == "*" or len(self.statuses) > 0
        if not roles_valid:
            error = "At least one role required"
            raise ValueError(error)
        if not statuses_valid:
            error = "At least one status required"
            raise ValueError(error)

    def is_satisfied_by(self, role: UserRole, status: UserStatus) -> bool:
        """
        Проверяет, удовлетворяет ли пользователь праву.

        Returns:
            true, если удовлетворяет.

        """
        return (self.roles == "*" or role in self.roles) and (self.statuses == "*" or status in self.statuses)

    def _get_equality_components(self) -> tuple[Any, ...]:
        return (self.roles, self.statuses)


class UserRights:
    """Каталог прав пользователей."""

    RESTORE_ACCOUNT: Final = UserRight(
        roles=UserRight.ALL,
        statuses={UserStatus.DELETED},
    )

    CHECK_USER_LIST: Final = UserRight(
        roles={UserRole.ADMIN, UserRole.MODERATOR},
        statuses={UserStatus.ACTIVE},
    )
    CHANGE_USER: Final = UserRight(
        roles={UserRole.ADMIN},
        statuses={UserStatus.ACTIVE},
    )
    CHANGE_SELF: Final = UserRight(
        roles={UserRole.USER, UserRole.MODERATOR},
        statuses={UserStatus.ACTIVE},
    )

    UPDATE_TASK: Final = UserRight(
        roles={UserRole.ADMIN, UserRole.MODERATOR},
        statuses={UserStatus.ACTIVE},
    )

    CHECK_SUBMISSION: Final = UserRight(
        roles={UserRole.ADMIN, UserRole.MODERATOR},
        statuses={UserStatus.ACTIVE},
    )
    SEND_SUBMISSION: Final = UserRight(
        roles={UserRole.USER},
        statuses={UserStatus.ACTIVE},
    )
