import re
from dataclasses import dataclass

from web_suffer.contexts.auth.domain.exceptions import InvalidEmailError
from web_suffer.shared.domain.value_objects.base_value_object import BaseValueObject
from web_suffer.shared.domain.value_objects.single_value_object import SingleValueObject

_EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9][\w.+-]*[a-zA-Z0-9]@[a-zA-Z][a-zA-Z0-9.\-]*[a-zA-Z]\.[a-zA-Z]{2,}")


@dataclass(frozen=True)
class UserEmail(SingleValueObject):
    """Value object почты пользователя."""

    value: str

    def __post_init__(self) -> None:
        """
        Нормализация и проверка формата.

        Raises:
            InvalidEmailError: строка не проходит проверку на формат почты

        """
        normalized = self.value.strip().lower()
        if ".." in normalized:
            raise InvalidEmailError(self.value)
        if not _EMAIL_PATTERN.fullmatch(normalized):
            raise InvalidEmailError(self.value)
        object.__setattr__(self, "value", normalized)

    def __eq__(self, obj: object) -> bool:  # noqa: D105
        return BaseValueObject.__eq__(self, obj)

    def __hash__(self) -> int:  # noqa: D105
        return BaseValueObject.__hash__(self)
