from typing import ClassVar

from web_suffer.contexts.tasks.domain import types
from web_suffer.shared.domain.value_objects.single_value_object import SingleValueObject


class SubmissionStatus(SingleValueObject):
    """Value object статуса посылки."""

    value: types.SubmissionStatus

    AWAIABLE: ClassVar["SubmissionStatus"]
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


SubmissionStatus.AWAIABLE = SubmissionStatus("available")
SubmissionStatus.PENDING = SubmissionStatus("pending")
SubmissionStatus.ACCEPTED = SubmissionStatus("accepted")
SubmissionStatus.REJECTED = SubmissionStatus("rejected")
