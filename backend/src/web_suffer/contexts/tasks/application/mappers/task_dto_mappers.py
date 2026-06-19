from typing import Protocol

from web_suffer.contexts.tasks.application.dtos.submission_dto import SubmissionDTO, SubmissionIDDTO
from web_suffer.contexts.tasks.application.dtos.task_dto import TaskDTO, TaskIDDTO, UsersTaskDTO
from web_suffer.contexts.tasks.application.dtos.usert_dto import UserTDTO
from web_suffer.contexts.tasks.domain import types
from web_suffer.contexts.tasks.domain.entities.submission import Submission
from web_suffer.contexts.tasks.domain.entities.task import Task
from web_suffer.contexts.tasks.domain.entities.user import UserT
from web_suffer.contexts.tasks.domain.types import TaskStatus
from web_suffer.contexts.tasks.domain.value_objects import submission_status
from web_suffer.contexts.tasks.domain.value_objects.submission_id import SubmissionID
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
    def to_subm_dto(subm: Submission) -> SubmissionDTO:
        """
        Domain Entity -> DTO.

        Returns:
            Immutable Submission DTO.

        """

    @staticmethod
    def to_user_dto(user: UserT) -> UserTDTO:
        """
        Domain Entity -> DTO.

        Returns:
            Immutable UserT DTO.

        """

    @staticmethod
    def from_task_id_dto(task_id: TaskIDDTO) -> TaskID:
        """
        DTO -> Domain value object.

        Returns:
            Domain TaskID value object.

        """

    @staticmethod
    def to_task_id_dto(task: TaskID) -> TaskIDDTO:
        """
        Domain value object -> DTO.

        Returns:
            Immutable Task ID DTO.

        """

    @staticmethod
    def from_subm_id_dto(task_id: SubmissionIDDTO) -> SubmissionID:
        """
        DTO -> Domain value object.

        Returns:
            Domain SubmissionID value object.

        """

    @staticmethod
    def to_subm_id_dto(task: SubmissionID) -> SubmissionIDDTO:
        """
        Domain value object -> DTO.

        Returns:
            Immutable Submission ID DTO.

        """

    @staticmethod
    def to_user_task_dto(task: Task, status: TaskStatus) -> UsersTaskDTO:
        """
        Domain Entity -> DTO.

        Returns:
            Immutable User's task DTO.

        """

    @staticmethod
    def from_status_dto(status: types.SubmissionStatus) -> submission_status.SubmissionStatus:
        """
        Strong type -> Domain value object.

        Returns:
            Domain SubmissionStatus value object.

        """
