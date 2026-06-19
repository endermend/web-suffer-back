from datetime import UTC, datetime

import structlog

from web_suffer.contexts.tasks.application.dtos.submission_dto import CreateSubmissionDTO, SubmissionIDDTO
from web_suffer.contexts.tasks.application.exceptions import ExpiredTaskError, InvalidTaskError
from web_suffer.contexts.tasks.application.mappers.task_dto_mappers import ITaskDTOMapper
from web_suffer.contexts.tasks.domain.entities.submission import Submission
from web_suffer.contexts.tasks.domain.repository.submission_repository import ISubmissionRepository
from web_suffer.contexts.tasks.domain.repository.task_repository import ITaskRepository
from web_suffer.contexts.tasks.domain.value_objects.submission_file import SubmissionFile
from web_suffer.contexts.tasks.domain.value_objects.task_id import TaskID
from web_suffer.shared.domain.exceptions import InsufficientPermissionsError
from web_suffer.shared.domain.interfaces.auth_service import IAuthService
from web_suffer.shared.domain.value_objects.user_rights import UserRights

logger = structlog.stdlib.get_logger()


class CreateSubmissionUseCase:
    """Use Case добавления нового отправления."""

    def __init__(
        self,
        task_repo: ITaskRepository,
        subm_repo: ISubmissionRepository,
        mapper: ITaskDTOMapper,
        auth_service: IAuthService,
    ) -> None:
        """Инициализация use case."""
        self._task_repo = task_repo
        self._subm_repo = subm_repo
        self._mapper = mapper
        self._auth_service = auth_service

    async def execute(self, input_dto: CreateSubmissionDTO) -> SubmissionIDDTO:
        """
        Добавляет новое задание.

        Returns:
            SubmissionIDDTO: id отправления.

        Raises:
            InsufficientPermissionsError: у пользователя недостаточно прав создавать отправление.
            InvalidTaskError: задания с таким id не существует.
            ExpiredTaskError: дедлайн задания уже прошел.

        """  # noqa: RUF002
        user_id = await self._auth_service.get_user_id_by_token(input_dto.access_token)
        if not await self._auth_service.check_user_right(user_id, UserRights.SEND_SUBMISSION):
            error = "Not enought permission."
            logger.warning("task.subm.failed", reason="not_enought_permission")
            raise InsufficientPermissionsError(error)

        task_id = TaskID(input_dto.task_id)
        task = await self._task_repo.get_by_id(task_id)
        if not task:
            logger.warning("task.subm.failed", reason="task_not_found")
            raise InvalidTaskError
        now = datetime.now(UTC)
        if task.deadline < now:
            logger.warning("task.subm.failed", reason="task_expired")
            raise ExpiredTaskError

        subm = Submission.create(
            task_id=task_id,
            user_id=user_id,
            content=input_dto.content,
            file=SubmissionFile(input_dto.file),
        )

        await self._subm_repo.save(subm)

        return self._mapper.to_subm_id_dto(subm.id)
