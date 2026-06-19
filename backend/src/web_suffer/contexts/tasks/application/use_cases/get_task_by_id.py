import structlog

from web_suffer.contexts.tasks.application.dtos.task_dto import TaskDTO, TaskIDDTO
from web_suffer.contexts.tasks.application.exceptions import InvalidTaskError
from web_suffer.contexts.tasks.application.mappers.task_dto_mappers import ITaskDTOMapper
from web_suffer.contexts.tasks.domain.repository.task_repository import ITaskRepository

logger = structlog.stdlib.get_logger()


class GetTaskByIDUseCase:
    """Use Case получение информации о задании по ID."""  # noqa: RUF002

    def __init__(
        self,
        task_repo: ITaskRepository,
        mapper: ITaskDTOMapper,
    ) -> None:
        """Инициализация use case."""
        self._task_repo = task_repo
        self._mapper = mapper

    async def execute(self, input_dto: TaskIDDTO) -> TaskDTO:
        """
        Возвращает полную информацию о задании по Task ID.

        Returns:
            TaskDTO: информация о задании.

        Raises:
            InvalidTaskError: задание с таким id не существует.

        """  # noqa: RUF002
        task = await self._task_repo.get_by_id(self._mapper.from_task_id_dto(input_dto))
        if not task:
            logger.warning("task.task.failed", reason="task_not_found")
            raise InvalidTaskError

        return self._mapper.to_task_dto(task)
