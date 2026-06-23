from abc import abstractmethod
from datetime import datetime
from typing import Protocol

from web_suffer.contexts.tasks.domain.entities.submission import Submission
from web_suffer.contexts.tasks.domain.types import SubmissionOrderByType
from web_suffer.contexts.tasks.domain.value_objects.submission_id import SubmissionID
from web_suffer.contexts.tasks.domain.value_objects.submission_status import SubmissionStatus
from web_suffer.contexts.tasks.domain.value_objects.task_id import TaskID
from web_suffer.shared.domain.value_objects.user_id import UserID


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
    async def get_list(
        self,
        user_id: UserID | None,
        status: SubmissionStatus | None = None,
        updated_after: datetime | None = None,
        order_by: SubmissionOrderByType | None = None,
    ) -> list[Submission]:
        """
        Получение Submission.

        Если submission_status не None, фильтрует по статусу
        """

    @abstractmethod
    async def check_pending(
        self,
        task_id: TaskID,
    ) -> bool:
        """Проверка на наличие отправлений ожидающих проверку."""
