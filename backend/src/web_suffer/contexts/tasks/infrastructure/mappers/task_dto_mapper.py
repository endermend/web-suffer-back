from typing import override

from web_suffer.contexts.tasks.application.dtos.submission_dto import SubmissionDTO, SubmissionIDDTO
from web_suffer.contexts.tasks.application.dtos.task_dto import TaskDTO, TaskIDDTO, UsersTaskDTO
from web_suffer.contexts.tasks.application.dtos.usert_dto import UserTDTO
from web_suffer.contexts.tasks.application.mappers.task_dto_mappers import ITaskDTOMapper
from web_suffer.contexts.tasks.domain import types
from web_suffer.contexts.tasks.domain.entities.submission import Submission
from web_suffer.contexts.tasks.domain.entities.task import Task
from web_suffer.contexts.tasks.domain.entities.user import UserT
from web_suffer.contexts.tasks.domain.types import TaskStatus
from web_suffer.contexts.tasks.domain.value_objects import submission_status
from web_suffer.contexts.tasks.domain.value_objects.submission_id import SubmissionID
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
    def to_subm_dto(subm: Submission) -> SubmissionDTO:
        """
        Domain Entity -> DTO.

        Returns:
            Immutable Submission DTO.

        """
        return SubmissionDTO(
            submission_id=subm.id.value,
            task_id=subm.task_id.value,
            user_id=subm.user_id.value,
            content=subm.content,
            file=subm.file.value,
            status=subm.status.value,
            comment=subm.admin_comment,
        )

    @staticmethod
    def to_user_dto(user: UserT) -> UserTDTO:
        """
        Domain Entity -> DTO.

        Returns:
            Immutable UserT DTO.

        """
        return UserTDTO(
            user_id=user.id.value,
            exp=user.exp,
            money=user.money,
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
    def from_subm_id_dto(subm_id: SubmissionIDDTO) -> SubmissionID:
        """
        DTO -> Domain value object.

        Returns:
            Domain SubmissionID value object.

        """
        return SubmissionID(value=subm_id.submission_id)

    @staticmethod
    def to_subm_id_dto(subm: SubmissionID) -> SubmissionIDDTO:
        """
        Domain value object -> DTO.

        Returns:
            Immutable Submission ID DTO.

        """
        return SubmissionIDDTO(
            submission_id=subm.value,
        )

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

    @staticmethod
    def from_status_dto(status: types.SubmissionStatus) -> submission_status.SubmissionStatus:
        """
        Strong type -> Domain value object.

        Returns:
            Domain SubmissionStatus value object.

        """
        return submission_status.SubmissionStatus(
            value=status,
        )
