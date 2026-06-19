
import structlog

from web_suffer.contexts.tasks.application.dtos.submission_dto import ChangeSubmissionDTO, SubmissionIDDTO
from web_suffer.contexts.tasks.application.exceptions import InvalidSubmissionError, InvalidTaskError
from web_suffer.contexts.tasks.application.interfaces.user_service import IUserService
from web_suffer.contexts.tasks.application.mappers.task_dto_mappers import ITaskDTOMapper
from web_suffer.contexts.tasks.domain.repository.submission_repository import ISubmissionRepository
from web_suffer.contexts.tasks.domain.repository.task_repository import ITaskRepository
from web_suffer.contexts.tasks.domain.value_objects.submission_id import SubmissionID
from web_suffer.contexts.tasks.domain.value_objects.submission_status import SubmissionStatus
from web_suffer.shared.domain.exceptions import InsufficientPermissionsError
from web_suffer.shared.domain.interfaces.auth_service import IAuthService
from web_suffer.shared.domain.value_objects.user_right import UserRights

logger = structlog.stdlib.get_logger()


class ChangeSubmissionUseCase:
    """Use Case изменения отправления."""

    def __init__(
        self,
        task_repo: ITaskRepository,
        subm_repo: ISubmissionRepository,
        mapper: ITaskDTOMapper,
        user_service: IUserService,
        auth_service: IAuthService,
    ) -> None:
        """Инициализация use case."""
        self._task_repo = task_repo
        self._subm_repo = subm_repo
        self._mapper = mapper
        self._user_service = user_service
        self._auth_service = auth_service

    async def execute(self, input_dto: ChangeSubmissionDTO) -> SubmissionIDDTO:
        """
        Добавляет новое задание.

        Returns:
            SubmissionIDDTO: id отправления.

        Raises:
            InsufficientPermissionsError: у пользователя недостаточно прав создавать отправление.
            InvalidTaskError: задания с таким id не существует.
            InvalidSubmissionError: отправления с таким id не существует.

        """  # noqa: RUF002
        user_id = await self._auth_service.get_user_id_by_token(input_dto.access_token)
        if not await self._auth_service.check_user_right(user_id, UserRights.CHECK_SUBMISSION):
            error = "Not enought permission."
            logger.warning("task.subm.failed", reason="not_enought_permission")
            raise InsufficientPermissionsError(error)

        subm_id = SubmissionID(input_dto.submission_id)
        subm = await self._subm_repo.get_by_id(subm_id)
        if not subm:
            logger.warning("task.subm.failed", reason="subm_not_found")
            raise InvalidSubmissionError

        task = await self._task_repo.get_by_id(subm.task_id)
        if not task:
            logger.error("task.subm.failed", reason="task_not_found")
            raise InvalidTaskError
        old_result = int(subm.status == SubmissionStatus.ACCEPTED)
        new_result = int(subm.status == SubmissionStatus.ACCEPTED)

        subm.set_status(input_dto.status)
        subm.set_comment(input_dto.comment)

        await self._subm_repo.save(subm)

        if old_result != new_result:
            await self._user_service.update_user_by_id(
                user_id=user_id,
                exp_diff=(new_result - old_result) * task.exp,
                money_diff=(new_result - old_result) * task.money,
            )

        return self._mapper.to_subm_id_dto(subm.id)
