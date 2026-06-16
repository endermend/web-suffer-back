from pathlib import Path
from typing import ClassVar

from web_suffer.shared.domain.value_objects.single_value_object import SingleValueObject


class SubmissionFile(SingleValueObject):
    """Файл посылки."""

    value: Path | None

    EMPTY: ClassVar["SubmissionFile"]

    def does_have_file(self) -> bool:
        """
        Есть ли файл к посылке.

        Returns:
            bool есть ли файл к послыке.

        """
        return self.value is not None


SubmissionFile.EMPTY = SubmissionFile(None)
