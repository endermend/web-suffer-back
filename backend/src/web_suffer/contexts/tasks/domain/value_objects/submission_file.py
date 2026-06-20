from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from web_suffer.shared.domain.value_objects.single_value_object import SingleValueObject


@dataclass(frozen=True)
class SubmissionFile(SingleValueObject):
    """Файл посылки."""

    value: Path | None

    EMPTY: ClassVar["SubmissionFile"]

    def does_have_file(self) -> bool:
        """
        Есть ли файл к посылке.

        Returns:
            bool есть ли файл к посылке.

        """
        return self.value is not None

    @classmethod
    def from_str(cls, posix_path: str) -> "SubmissionFile":
        """
        Востановление файла из строки.

        Returns:
            Путь файла.

        """
        return cls(
            value=Path(posix_path),
        )


SubmissionFile.EMPTY = SubmissionFile(None)
