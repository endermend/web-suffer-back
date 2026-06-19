from web_suffer.contexts.tasks.domain.entities.submission import Submission
from web_suffer.contexts.tasks.domain.value_objects.submission_file import SubmissionFile
from web_suffer.contexts.tasks.domain.value_objects.submission_id import SubmissionID
from web_suffer.contexts.tasks.domain.value_objects.submission_status import SubmissionStatus
from web_suffer.contexts.tasks.domain.value_objects.task_id import TaskID
from web_suffer.contexts.tasks.infrastructure.persistence.models.submission_model import SubmissionORMModel
from web_suffer.shared.domain.value_objects.user_id import UserID


class SubmissionORMMapper:
    """Mapper между Domain Entity и ORM model."""

    @staticmethod
    def to_domain(orm: SubmissionORMModel) -> Submission:
        """
        ORM Model -> Domain Entity.

        Returns:
            Отправление из бд.

        """
        return Submission.hydrate(
            id=SubmissionID(orm.id),
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            task_id=TaskID(orm.task_id),
            user_id=UserID(orm.user_id),
            content=orm.content,
            file=SubmissionFile.from_str(orm.file) if orm.file else SubmissionFile.EMPTY,
            status=SubmissionStatus(orm.status),
            comment=orm.admin_comment,
        )

    @staticmethod
    def update_from_domain(
        orm: SubmissionORMModel,
        entity: Submission,
    ) -> None:
        """Обновление существующей ORM модели из Domain."""
        orm.id = entity.id.value
        orm.updated_at = entity.updated_at
        orm.task_id = entity.task_id.value
        orm.user_id = entity.user_id.value
        orm.content = entity.content
        orm.file = entity.file.value.as_posix() if entity.file.value else None
        orm.status = entity.status.value
        orm.admin_comment = entity.admin_comment
