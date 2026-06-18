from abc import abstractmethod
from typing import Protocol

from web_suffer.contexts.tasks.domain.entities.submission import Submission
from web_suffer.contexts.tasks.domain.value_objects.submission_id import SubmissionID
from web_suffer.contexts.tasks.domain.value_objects.submission_status import SubmissionStatus


class ISubmissionRepository(Protocol):
    """Протокол Submission репозитория."""

    @abstractmethod
    async def save(self, submission: Submission) -> None:
        """Сохранение Submission."""

    @abstractmethod
    async def get_by_id(self, submission_id: SubmissionID) -> Submission | None:
        """
        Получение Submission по SubmissionID.

        None, если submission не найден.
        """

    @abstractmethod
    async def get_list(self, status: SubmissionStatus | None = None) -> list[Submission]:
        """
        Получение Submission.

        Если submission_status не None, фильтрует по статусу
        """
