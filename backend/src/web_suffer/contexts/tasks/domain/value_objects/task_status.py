from typing import ClassVar

from web_suffer.shared.domain.value_objects.single_value_object import SingleValueObject


class TaskStatus(SingleValueObject):
    """Value object статуса пользователя."""

    value: int

    ACTIVE: ClassVar["TaskStatus"]
    FINISHED: ClassVar["TaskStatus"]

    def is_active(self) -> bool:
        """
        Активно ли еще задание.

        Задание можно сдать, если оно еще активно.

        Returns:
            True, если задание активно.

        """
        return self.value == TaskStatus.ACTIVE.value


TaskStatus.ACTIVE = TaskStatus(0)
TaskStatus.FINISHED = TaskStatus(1)
