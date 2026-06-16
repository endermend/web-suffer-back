from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Self, TypeVar

from web_suffer.shared.domain.value_objects.base_id import BaseID

R = TypeVar("R")


@dataclass(slots=True)
class BaseEntity:
    """Базовый класс доменной сущности."""

    _id: BaseID
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

    def __eq__(self, value: object) -> bool:
        """
        Сущности сравниваются по идентичности (DDD).

        Returns:
            Результат сравнения по self.id

        """
        if not isinstance(value, Self):
            return NotImplemented
        return self._id == value._id

    def __hash__(self) -> int:
        """
        Сущности хэшируются по идентичности (DDD).

        Returns:
            Хеш по self.id

        """
        return hash(self._id)
