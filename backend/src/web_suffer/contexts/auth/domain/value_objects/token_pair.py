from dataclasses import dataclass
from typing import Any

from web_suffer.contexts.auth.domain.value_objects.token import Token
from web_suffer.shared.domain.value_objects.base_value_object import BaseValueObject


@dataclass(slots=True, frozen=True)
class TokenPair(BaseValueObject):
    """VO пары токенов (Value Object DDD)."""

    access_token: Token
    refresh_token: Token

    def _get_equality_components(self) -> tuple[Any, ...]:
        return (self.access_token, self.refresh_token)
