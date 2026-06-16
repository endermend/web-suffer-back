from typing import ClassVar

from web_suffer.shared.domain.value_objects.single_value_object import SingleValueObject


class SubmissionStatus(SingleValueObject):
    """Value object статуса посылки."""

    value: str

    PENDING: ClassVar["SubmissionStatus"]
    ACCEPTED: ClassVar["SubmissionStatus"]
    REJECTED: ClassVar["SubmissionStatus"]

    def is_pending(self) -> bool:
        """
        Активно ли еще задание.

        Задание можно сдать, если оно еще активно.

        Returns:
            True, если задание активно.

        """
        return self.value == SubmissionStatus.PENDING.value


SubmissionStatus.PENDING = SubmissionStatus("На проверке")
SubmissionStatus.ACCEPTED = SubmissionStatus("Принято")
SubmissionStatus.REJECTED = SubmissionStatus("Не принято")
