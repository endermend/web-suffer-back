import structlog

from web_suffer.contexts.tasks.application.dtos.task_dto import TaskIDDTO, UpdateTaskDTO
from web_suffer.contexts.tasks.application.exceptions import UpdateForbidenError
from web_suffer.contexts.tasks.application.mappers.task_dto_mappers import ITaskDTOMapper
from web_suffer.contexts.tasks.domain.entities.task import Task
from web_suffer.contexts.tasks.domain.repository.submission_repository import ISubmissionRepository
from web_suffer.contexts.tasks.domain.repository.task_repository import ITaskRepository
from web_suffer.contexts.tasks.domain.value_objects.task_id import TaskID
from web_suffer.shared.domain.exceptions import InsufficientPermissionsError
from web_suffer.shared.domain.interfaces.auth_service import IAuthService
from web_suffer.shared.domain.value_objects.user_rights import UserRights

logger = structlog.stdlib.get_logger()


class UpdateTaskUseCase:
    """Use Case добавления нового/изменение задания."""

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

    async def execute(self, input_dto: UpdateTaskDTO) -> TaskIDDTO:
        """
        Добавляет новое задание.

        Если указано ID и такое задание существует, изменяет задание.

        Returns:
            TaskIDDTO: id задания.

        Raises:
            InsufficientPermissionsError: Недостаточно прав для создания/изменения задания.
            UpdateForbidenError: Обновление задания недоступно.

        """
        user_id = await self._auth_service.get_user_id_by_token(input_dto.access_token)
        if not await self._auth_service.check_user_right(user_id=user_id, right=UserRights.UPDATE_TASK):
            error = "Not enought permission."
            logger.warning("task.create.failed", reason="not_enought_permission")
            raise InsufficientPermissionsError(error)

        task_id = TaskID(input_dto.task_id) if input_dto.task_id else None
        if task_id and self._subm_repo.check_pending(task_id):
            raise UpdateForbidenError

        task = Task.create(
            id=task_id,
            title=input_dto.title,
            description=input_dto.description,
            deadline=input_dto.deadline,
            exp=input_dto.exp,
            money=input_dto.money,
        )

        await self._task_repo.save(task)

        return self._mapper.to_task_id_dto(task.id)
