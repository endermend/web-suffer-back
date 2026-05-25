from abc import ABC, abstractmethod
from typing import Any


class BaseValueObject(ABC):
    """Базовый класс для Value Objects."""

    @abstractmethod
    def _get_equality_components(self) -> tuple[Any, ...]:
        """
        Определение равенства двух VO.

        Returns:
            Кортеж, определяющий равенство.

        """

    def __eq__(self, other: object) -> bool:  # noqa: D105
        if not isinstance(other, self.__class__):
            return False
        return self._get_equality_components() == other._get_equality_components()

    def __hash__(self) -> int:  # noqa: D105
        return hash(self._get_equality_components())

    def __ne__(self, other: object) -> bool:  # noqa: D105
        return not self.__eq__(other)

    def __repr__(self) -> str:  # noqa: D105
        components = self._get_equality_components()
        return ", ".join(repr(c) for c in components)
