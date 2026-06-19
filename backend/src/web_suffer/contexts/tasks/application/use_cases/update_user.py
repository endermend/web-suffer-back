import structlog

from web_suffer.contexts.tasks.application.dtos.usert_dto import UpdateUserTDTO
from web_suffer.contexts.tasks.application.interfaces.user_service import IUserService
from web_suffer.contexts.tasks.application.mappers.task_dto_mappers import ITaskDTOMapper
from web_suffer.shared.domain.exceptions import InsufficientPermissionsError
from web_suffer.shared.domain.interfaces.auth_service import IAuthService
from web_suffer.shared.domain.value_objects.user_id import UserID
from web_suffer.shared.domain.value_objects.user_rights import UserRights

logger = structlog.stdlib.get_logger()


class UpdateUserUseCase:
    """Use Case обновления пользователя."""

    def __init__(
            self,
            user_service: IUserService,
            mapper: ITaskDTOMapper,
            auth_service: IAuthService,
        ) -> None:
        """Инициализация use case."""
        self._user_service = user_service
        self._mapper = mapper
        self._auth_service = auth_service

    async def execute(self, input_dto: UpdateUserTDTO) -> None:
        """
        Обновляет параметры пользователя.

        Если пользователя не существует, создает нового.

        Raises:
            InsufficientPermissionsError: Недостаточно прав для изменения пользователя.

        """
        user_id = await self._auth_service.get_user_id_by_token(input_dto.access_token)
        if not await self._auth_service.check_user_right(user_id=user_id, right=UserRights.CHANGE_USER):
            error = "Not enought permission."
            logger.warning("task.create.failed", reason="not_enought_permission")
            raise InsufficientPermissionsError(error)

        update_user_id = UserID(input_dto.user_id)
        if not await self._auth_service.check_user_right(user_id=update_user_id, right=UserRights.TO_EXISTS):
            error = "Not enought permission."
            logger.warning("task.create.failed", reason="not_enought_permission")
            raise InsufficientPermissionsError(error)

        await self._user_service.update_user_by_id(
            user_id=update_user_id,
            exp_diff=input_dto.exp_diff,
            money_diff=input_dto.money_diff,
        )
