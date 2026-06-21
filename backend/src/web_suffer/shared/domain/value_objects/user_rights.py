from typing import Final

from web_suffer.shared.domain.value_objects.user_right import UserRight
from web_suffer.shared.domain.value_objects.user_role import UserRole
from web_suffer.shared.domain.value_objects.user_status import UserStatus


class UserRights:
    """Каталог прав пользователей."""

    TO_EXISTS: Final = UserRight(
        roles=UserRight.ALL,
        statuses=UserRight.ALL,
    )

    DELETE_ACCOUNT: Final = UserRight(
        roles=UserRight.ALL,
        statuses={UserStatus.ACTIVE},
    )
    RESTORE_ACCOUNT: Final = UserRight(
        roles=UserRight.ALL,
        statuses={UserStatus.DELETED},
    )

    CHECK_USER_LIST: Final = UserRight(
        roles={UserRole.ADMIN, UserRole.MODERATOR},
        statuses={UserStatus.ACTIVE},
    )
    VIEW_USER: Final = UserRight(
        roles={UserRole.MODERATOR, UserRole.ADMIN},
        statuses={UserStatus.ACTIVE},
    )

    CHANGE_RESTRICTED_USER: Final = UserRight(
        roles={UserRole.ADMIN},
        statuses={UserStatus.ACTIVE},
    )
    CHANGE_USER: Final = UserRight(
        roles={UserRole.ADMIN},
        statuses={UserStatus.ACTIVE},
    )
    CHANGE_SELF: Final = UserRight(
        roles={UserRole.USER, UserRole.MODERATOR},
        statuses={{UserStatus.DELETED, UserStatus.ACTIVE},
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
