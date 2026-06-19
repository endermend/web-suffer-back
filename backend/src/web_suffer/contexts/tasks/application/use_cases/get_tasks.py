import structlog

from web_suffer.contexts.tasks.application.dtos.task_dto import UsersTaskDTO, UsersTasksRangeDTO
from web_suffer.contexts.tasks.application.mappers.task_dto_mappers import ITaskDTOMapper
from web_suffer.contexts.tasks.domain.repository.task_repository import ITaskRepository
from web_suffer.shared.domain.interfaces.auth_service import IAuthService

logger = structlog.stdlib.get_logger()


class GetTasksUseCase:
    """Use Case получения информации о заданиях по фильтру."""  # noqa: RUF002

    def __init__(
            self,
            task_repo: ITaskRepository,
            mapper: ITaskDTOMapper,
            auth_service: IAuthService,
        ) -> None:
        """Инициализация use case."""
        self._task_repo = task_repo
        self._mapper = mapper
        self._auth_service = auth_service

    async def execute(self, input_dto: UsersTasksRangeDTO) -> list[UsersTaskDTO]:
        """
        Возвращает информацию о заданиях пользователя по заданному фильтру.

        Returns:
            list[UsersTaskDTO]: информация о задании пользователя.

        """  # noqa: RUF002
        user_id = await self._auth_service.get_user_id_by_token(input_dto.access_token)
        tasks = await self._task_repo.get_list(
            user_id=user_id,
            deadline_from=input_dto.deadline_from,
            deadline_till=input_dto.deadline_till,
            status=input_dto.status,
            order_by=input_dto.order_by,
            limit=input_dto.limit,
            offset=input_dto.offset,
        )

        return [
            self._mapper.to_user_task_dto(task=task, status=status)
            for task, status in tasks
        ]
