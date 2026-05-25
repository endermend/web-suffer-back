from uuid import UUID, uuid4

from web_suffer.shared.domain.value_objects.single_value_object import SingleValueObject


class UserID(SingleValueObject):
    """Value object ID пользователя."""

    value: UUID

    @classmethod
    def new(cls) -> "UserID":
        """
        Генерация нового UserID.

        Returns:
            UserID

        """
        return cls(uuid4())

    @classmethod
    def from_str(cls, uuid_str: str) -> "UserID":
        """
        Получение UserID из строки str.

        Returns:
            UserID

        """
        return cls(UUID(uuid_str))
