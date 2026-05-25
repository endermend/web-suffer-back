from dishka import (
    Provider,
    Scope,
    provide,  # pyright: ignore[reportUnknownVariableType]
)

from web_suffer.contexts.auth.application.mappers.auth_dto_mapper import IAuthDTOMapper
from web_suffer.contexts.auth.application.use_cases import (
    GetLoginByAccessTokenUseCase,
    LoginUserUseCase,
    RefreshUserUseCase,
    RegisterUserUseCase,
)
from web_suffer.contexts.auth.application.use_cases.get_userid import GetUserIDByAccessTokenUseCase
from web_suffer.contexts.auth.infrastructure.mappers.auth_dto_mapper import AuthDTOMapper


class AuthUseCasesProvider(Provider):
    """Провайдер для всей Auth UseCase."""

    scope = Scope.REQUEST

    auth_dto_mapper = provide(
        AuthDTOMapper,
        provides=IAuthDTOMapper,
        scope=Scope.APP,
    )

    register_user = provide(RegisterUserUseCase)
    login_user = provide(LoginUserUseCase)
    refresh_user = provide(RefreshUserUseCase)
    get_login_by_token = provide(GetLoginByAccessTokenUseCase)
    get_userid_by_token = provide(GetUserIDByAccessTokenUseCase)
