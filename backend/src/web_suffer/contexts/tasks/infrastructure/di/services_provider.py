from dishka import Provider, Scope, provide

from web_suffer.contexts.tasks.application.interfaces.user_service import IUserService
from web_suffer.contexts.tasks.domain.repository.user_repository import IUserTRepository
from web_suffer.contexts.tasks.infrastructure.services.user_service import UserService


class ServiceProvider(Provider):
    """Провайдер, объединяющий провайдеры заданий."""

    @provide(scope=Scope.REQUEST)
    @staticmethod
    def get_user_service(
        user_repository: IUserTRepository,
    ) -> IUserService:
        """
        Провайдер для ITokenService.

        Returns:
            TokenService: реализация ITokenService

        """
        return UserService(user_repository=user_repository)
