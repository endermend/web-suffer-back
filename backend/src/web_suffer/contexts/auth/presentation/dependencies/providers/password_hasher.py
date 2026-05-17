from dishka import (
    Provider,
    Scope,
    provide,  # pyright: ignore[reportUnknownVariableType]
)

from web_suffer.contexts.auth.domain.security import IPasswordHasher
from web_suffer.contexts.auth.infrastructure.security import PasswordHasher


class PasswordHasherProvider(Provider):
    """Провайдер для PasswordHasher."""

    password_hasher = provide(
        PasswordHasher,
        scope=Scope.APP,
        provides=IPasswordHasher,
    )
