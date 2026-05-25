from dataclasses import dataclass
from typing import Any

from web_suffer.shared.domain.value_objects.base_value_object import BaseValueObject


@dataclass(slots=True, frozen=True)
class SingleValueObject(BaseValueObject):
    """Базовый Single Value Object."""

    value: Any

    def _get_equality_components(self) -> tuple[Any, ...]:
        return (self.value, )
