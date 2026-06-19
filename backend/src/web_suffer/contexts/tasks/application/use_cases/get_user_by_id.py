import structlog

from web_suffer.contexts.tasks.application.dtos.usert_dto import UserTDTO, UserTIDDTO
from web_suffer.contexts.tasks.application.interfaces.user_service import IUserService
from web_suffer.contexts.tasks.application.mappers.task_dto_mappers import ITaskDTOMapper
from web_suffer.contexts.tasks.domain.repository.user_repository import IUserTRepository
from web_suffer.shared.domain.exceptions import DomainError, InsufficientPermissionsError
from web_suffer.shared.domain.interfaces.auth_service import IAuthService
from web_suffer.shared.domain.value_objects.user_id import UserID
from web_suffer.shared.domain.value_objects.user_rights import UserRights

logger = structlog.stdlib.get_logger()


class GetUserByIDUseCase:
    """Use Case получения информации пользователя по id."""

    def __init__(
            self,
            user_repo: IUserTRepository,
            user_service: IUserService,
            mapper: ITaskDTOMapper,
            auth_service: IAuthService,
        ) -> None:
        """Инициализация use case."""
        self._user_repo = user_repo
        self._user_service = user_service
        self._mapper = mapper
        self._auth_service = auth_service

    async def execute(self, input_dto: UserTIDDTO) -> UserTDTO:
        """
        Получает информацию пользователя по id.

        Returns:
            UserTDTO: информация пользователя.

        Raises:
            InsufficientPermissionsError: Недостаточно прав для просмотра информации пользователя.
            DomainError: Не удалось создать пользователя.

        """  # noqa: RUF002
        user_id = await self._auth_service.get_user_id_by_token(input_dto.access_token)
        info_user_id = UserID(input_dto.user_id)
        if user_id != info_user_id and not await self._auth_service.check_user_right(user_id=user_id, right=UserRights.VIEW_USER):
            error = "Not enought permission."
            logger.warning("task.create.failed", reason="not_enought_permission")
            raise InsufficientPermissionsError(error)

        user = await self._user_repo.get_by_id(info_user_id)
        update_user_id = UserID(input_dto.user_id)
        if user is None:
            if not await self._auth_service.check_user_right(user_id=update_user_id, right=UserRights.TO_EXISTS):
                error = "Not enought permission."
                logger.warning("task.create.failed", reason="not_enought_permission")
                raise InsufficientPermissionsError(error)

            await self._user_service.update_user_by_id(update_user_id, 0, 0)
        user = await self._user_repo.get_by_id(info_user_id)
        if user is None:
            error = "Could not create user."
            logger.warning("task.create.failed", reason="can_not_create_user")
            raise DomainError
        return self._mapper.to_user_dto(user=user)
