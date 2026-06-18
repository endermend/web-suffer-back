from uuid import UUID

from web_suffer.shared.domain.value_objects.base_id import BaseID


class UserID(BaseID):
    """Value object ID пользователя."""

    value: UUID
