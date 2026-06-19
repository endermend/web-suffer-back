from typing import override

from web_suffer.contexts.tasks.application.dtos.task_dto import TaskDTO, TaskIDDTO, UsersTaskDTO
from web_suffer.contexts.tasks.application.mappers.task_dto_mappers import ITaskDTOMapper
from web_suffer.contexts.tasks.domain.entities.task import Task
from web_suffer.contexts.tasks.domain.types import TaskStatus
from web_suffer.contexts.tasks.domain.value_objects.task_id import TaskID


class TaskDTOMapper(ITaskDTOMapper):
    """Mapper между Domain Entity и DTO."""

    @staticmethod
    @override
    def to_task_dto(task: Task) -> TaskDTO:
        """
        Domain Entity -> DTO.

        Returns:
            Immutable Task DTO.

        """
        return TaskDTO(
            task_id=task.id.value,
            title=task.title,
            description=task.description,
            deadline=task.deadline,
            exp=task.exp,
            money=task.money,
        )

    @staticmethod
    @override
    def from_task_id_dto(task_id: TaskIDDTO) -> TaskID:
        """
        DTO -> Domain value object.

        Returns:
            Domain TaskID value object.

        """
        return TaskID(value=task_id.task_id)

    @staticmethod
    @override
    def to_task_id_dto(task: TaskID) -> TaskIDDTO:
        """
        Domain value object -> DTO.

        Returns:
            Immutable Task ID DTO.

        """
        return TaskIDDTO(task.value)

    @staticmethod
    @override
    def to_user_task_dto(task: Task, status: TaskStatus) -> UsersTaskDTO:
        """
        Domain Entity -> DTO.

        Returns:
            Immutable User's task DTO.

        """
        return UsersTaskDTO(
            task_id=task.id.value,
            title=task.title,
            description=task.description,
            deadline=task.deadline,
            exp=task.exp,
            money=task.money,
            status=status,
        )
