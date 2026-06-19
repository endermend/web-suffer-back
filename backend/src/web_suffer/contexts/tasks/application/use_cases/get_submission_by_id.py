import structlog

from web_suffer.contexts.tasks.application.dtos.submission_dto import SubmissionDTO, SubmissionIDDTO
from web_suffer.contexts.tasks.application.exceptions import InvalidSubmissionError
from web_suffer.contexts.tasks.application.mappers.task_dto_mappers import ITaskDTOMapper
from web_suffer.contexts.tasks.domain.repository.submission_repository import ISubmissionRepository
from web_suffer.shared.domain.exceptions import InsufficientPermissionsError
from web_suffer.shared.domain.interfaces.auth_service import IAuthService
from web_suffer.shared.domain.value_objects.user_right import UserRights

logger = structlog.stdlib.get_logger()


class GetSubmissionByIDUseCase:
    """Use Case получение информации об отправлении по ID."""  # noqa: RUF002

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

    async def execute(self, input_dto: SubmissionIDDTO) -> SubmissionDTO:
        """
        Возвращает полную информацию о задании по Submission ID.

        Returns:
            SubmissionDTO: информация о задании.

        Raises:
            InvalidSubmissionError: отправления с таким id не существует.
            InsufficientPermissionsError: у пользователя недостаточно прав просматривать отправление.

        """  # noqa: RUF002
        user_id = await self._auth_service.get_user_id_by_token(input_dto.access_token)
        subm = await self._subm_repo.get_by_id(self._mapper.from_subm_id_dto(input_dto))
        if not subm:
            logger.warning("task.subm.failed", reason="submission_not_found")
            raise InvalidSubmissionError

        if subm.user_id != user_id and not await self._auth_service.check_user_right(user_id, UserRights.CHECK_SUBMISSION):
            error = "Not enought permission."
            logger.warning("task.subm.failed", reason="not_enought_permission")
            raise InsufficientPermissionsError(error)

        return self._mapper.to_subm_dto(subm)
