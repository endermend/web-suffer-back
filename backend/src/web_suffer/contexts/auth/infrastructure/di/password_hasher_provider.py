from dishka import (
    Provider,
    Scope,
    provide,
)

from web_suffer.contexts.auth.application.interfaces.password_hasher import (
    IPasswordHasher,
)
from web_suffer.contexts.auth.infrastructure.services.password_hasher import ArgonPasswordHasher


class PasswordHasherProvider(Provider):
    """Провайдер для PasswordHasher."""

    password_hasher = provide(
        ArgonPasswordHasher,
        scope=Scope.APP,
        provides=IPasswordHasher,
    )
