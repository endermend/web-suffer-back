import structlog

from web_suffer.contexts.tasks.application.dtos.submission_dto import SubmissionDTO, SubmissionRangesDTO
from web_suffer.contexts.tasks.application.mappers.task_dto_mappers import ITaskDTOMapper
from web_suffer.contexts.tasks.domain.repository.submission_repository import ISubmissionRepository
from web_suffer.shared.domain.exceptions import InsufficientPermissionsError
from web_suffer.shared.domain.interfaces.auth_service import IAuthService
from web_suffer.shared.domain.value_objects.user_id import UserID
from web_suffer.shared.domain.value_objects.user_rights import UserRights

logger = structlog.stdlib.get_logger()


class GetSubmissionsUseCase:
    """Use Case получения информации об отправлениях по фильтру."""  # noqa: RUF002

    def __init__(
        self,
        subm_repo: ISubmissionRepository,
        mapper: ITaskDTOMapper,
        auth_service: IAuthService,
    ) -> None:
        """Инициализация use case."""
        self._subm_repo = subm_repo
        self._mapper = mapper
        self._auth_service = auth_service

    async def execute(self, input_dto: SubmissionRangesDTO) -> list[SubmissionDTO]:
        """
        Возвращает информацию об отправлениях пользователя/пользователей по заданному фильтру.

        Returns:
            list[UsersTaskDTO]: информация о задании пользователя.

        Raises:
            InsufficientPermissionsError: недостаточно прав просматривать чужие отправления.

        """  # noqa: RUF002
        user_id = await self._auth_service.get_user_id_by_token(input_dto.access_token)
        filter_user_id = UserID(input_dto.user_id) if input_dto.user_id is not None else None
        if user_id != filter_user_id and not await self._auth_service.check_user_right(user_id, UserRights.CHECK_SUBMISSION):
            error = "Not enought permission."
            logger.warning("task.create.failed", reason="not_enought_permission")
            raise InsufficientPermissionsError(error)

        subms = await self._subm_repo.get_list(
            user_id=filter_user_id,
            status=self._mapper.from_status_dto(input_dto.status) if input_dto.status is not None else None,
            order_by=input_dto.order_by,
        )
        return [self._mapper.to_subm_dto(subm=subm) for subm in subms]
