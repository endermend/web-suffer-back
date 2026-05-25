import re

from web_suffer.contexts.auth.domain.exceptions import InvalidEmailError
from web_suffer.shared.domain.value_objects.single_value_object import SingleValueObject

_EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._+-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")


class UserEmail(SingleValueObject):
    """Value object почты пользователя."""

    value: str

    def __post_init__(self) -> None:
        """
        Нормалиция и проверка формата.

        Raises:
            InvalidEmailError: строка не проходит проверку на формат почты

        """
        normalized = self.value.strip().lower()
        if not _EMAIL_PATTERN.fullmatch(normalized):
            raise InvalidEmailError(self.value)
        object.__setattr__(self, "value", normalized)
