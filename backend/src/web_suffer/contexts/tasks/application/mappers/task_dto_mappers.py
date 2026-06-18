from typing import Protocol

from web_suffer.contexts.tasks.application.dtos.task_dto import TaskDTO, TaskIDDTO
from web_suffer.contexts.tasks.domain.entities.task import Task
from web_suffer.contexts.tasks.domain.value_objects.task_id import TaskID


class ITaskDTOMapper(Protocol):
    """Mapper между Domain Entity и DTO."""

    @staticmethod
    def to_task_dto(task: Task) -> TaskDTO:
        """
        Domain Entity -> DTO.

        Returns:
            Immutable Task DTO.

        """

    @staticmethod
    def from_id_dto(task_id: TaskIDDTO) -> TaskID:
        """
        DTO -> Domain value object.

        Returns:
            Domain TaskID value object.

        """
