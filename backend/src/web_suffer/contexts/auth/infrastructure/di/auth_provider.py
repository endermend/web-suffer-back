from dishka import Provider

from web_suffer.contexts.auth.infrastructure.di.cookie_provider import CookieServiceProvider
from web_suffer.contexts.auth.infrastructure.di.db_provider import DBProvider
from web_suffer.contexts.auth.infrastructure.di.password_hasher_provider import PasswordHasherProvider
from web_suffer.contexts.auth.infrastructure.di.token_provider import TokenProvider
from web_suffer.contexts.auth.infrastructure.di.use_case_provider import AuthUseCasesProvider


class AuthProvider(
    AuthUseCasesProvider,
    CookieServiceProvider,
    DBProvider,
    PasswordHasherProvider,
    TokenProvider,
    Provider,
):
    """Провайдер, объединяющий провадеры аунтификации."""
