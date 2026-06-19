from collections import Counter
from datetime import UTC, datetime
from typing import TYPE_CHECKING

import structlog

from web_suffer.contexts.tasks.application.dtos.task_dto import TaskStatisticsDTO
from web_suffer.contexts.tasks.application.mappers.task_dto_mappers import ITaskDTOMapper
from web_suffer.contexts.tasks.domain.repository.task_repository import ITaskRepository
from web_suffer.shared.application.dtos.access_token_dto import PublicAccessTokenDTO
from web_suffer.shared.domain.interfaces.auth_service import IAuthService

if TYPE_CHECKING:
    from web_suffer.contexts.tasks.domain.types import TaskStatus

logger = structlog.stdlib.get_logger()


class GetTasksUseCase:
    """Use Case получения статистики по заданиям."""

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

    async def execute(self, input_dto: PublicAccessTokenDTO) -> TaskStatisticsDTO:
        """
        Возвращает статистику заданий.

        Returns:
            TaskStatisticsDTO: информация о заданиях. done_ None если пользователь не указан.

        """  # noqa: RUF002
        now = datetime.now(UTC)
        tasks_all = len(
            await self._task_repo.get_unathorized_list(
                deadline_till=now,
            ),
        )
        tasks_status: dict[TaskStatus, int] | None = None
        if input_dto.access_token is not None:
            user_id = await self._auth_service.get_user_id_by_token(input_dto.access_token)
            tasks = await self._task_repo.get_list(
                user_id=user_id,
                deadline_till=now,
            )
            tasks_status = dict(
                Counter(status for _, status in tasks),
            )

        return TaskStatisticsDTO(
            tasks_all=tasks_all,
            tasks_status=tasks_status,
        )
