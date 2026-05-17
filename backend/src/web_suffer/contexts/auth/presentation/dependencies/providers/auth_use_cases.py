from dishka import (
    Provider,
    Scope,
    provide,  # pyright: ignore[reportUnknownVariableType]
)

from web_suffer.contexts.auth.application.use_cases import (
    GetLoginUseCase,
    LoginUserUseCase,
    RefreshUserUseCase,
    RegisterUserUseCase,
)


class AuthUseCasesProvider(Provider):
    """Провайдер для всей Auth UseCase."""

    scope = Scope.REQUEST

    register_user = provide(RegisterUserUseCase)
    login_user = provide(LoginUserUseCase)
    refresh_user = provide(RefreshUserUseCase)
    get_email = provide(GetLoginUseCase)
