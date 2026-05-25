from dishka import (
    Provider,
    Scope,
    provide,
)

from web_suffer.contexts.auth.infrastructure.services.cookie_service import CookieService


class CookieServiceProvider(Provider):
    """Провайдер для CookieService."""

    cookie_service = provide(CookieService, scope=Scope.APP)
