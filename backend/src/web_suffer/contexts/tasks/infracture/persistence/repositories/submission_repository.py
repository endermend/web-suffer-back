from web_suffer.contexts.tasks.domain.entities.submission import Submission
from web_suffer.contexts.tasks.domain.repository.submission_repository import ISubmissionRepository
from web_suffer.contexts.tasks.domain.value_objects.submission_id import SubmissionID
from web_suffer.contexts.tasks.domain.value_objects.submission_status import SubmissionStatus


class SubmissionRepository(ISubmissionRepository):
    """Реализация Submission репозитория."""

    async def save(self, submission: Submission) -> None:
        """Сохранение Submission."""

    async def get_submission_by_id(self, task_id: SubmissionID) -> Submission | None:
        """
        Получение Submission по SubmissionID.

        None, если submission не найден.
        """

    async def get_tasks_list(self, submission_status: SubmissionStatus | None = None) -> list[Submission]:
        """
        Получение Submission.

        Если submission_status не None, фильтрует по статусу
        """
