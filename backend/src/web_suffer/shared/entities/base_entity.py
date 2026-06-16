from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TypeVar

R = TypeVar("R")


@dataclass(slots=True)
class BaseEntity:
    """Базовый класс доменной сущности."""

    _created_at: datetime
    _updated_at: datetime

    @property
    def created_at(self) -> datetime:
        """Дата создания пользователя."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Дата обновления пользователя."""
        return self._updated_at

    @staticmethod
    def update(
        func: Callable[..., R],
    ) -> Callable[..., R]:
        """Декоратор для обновления временной метки обновления пользователя."""  # noqa: DOC201

        def wrapper(self: BaseEntity, *args: None, **kwargs: None) -> R:
            result = func(self, *args, **kwargs)

            self._updated_at = datetime.now(UTC)
            return result

        return wrapper
