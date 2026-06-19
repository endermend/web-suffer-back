# contexts/auth/infrastructure/di/providers.py
from dishka import Provider, Scope, provide

from web_suffer.contexts.auth.application.mappers.auth_dto_mapper import IAuthDTOMapper
from web_suffer.contexts.auth.application.use_cases.get_userid import GetUserIDByAccessTokenUseCase
from web_suffer.contexts.auth.domain.repositories.user_repository import IUserRepository
from web_suffer.contexts.auth.infrastructure.services.adapter_service import AuthServiceAdapter
from web_suffer.shared.domain.interfaces.auth_service import IAuthService


class AdapterProvider(Provider):
    """Провайдер для контекста auth."""

    @provide(scope=Scope.REQUEST)
    @staticmethod
    def get_auth_service_adapter(
        get_user_id_use_case: GetUserIDByAccessTokenUseCase,
        user_repo: IUserRepository,
        mapper: IAuthDTOMapper,
    ) -> IAuthService:
        """
        Провайдер для IAuthService.

        Returns:
            AuthServiceAdapter: реализация IAuthService

        """
        return AuthServiceAdapter(
            get_user_id_use_case=get_user_id_use_case,
            user_repo=user_repo,
            mapper=mapper,
        )
