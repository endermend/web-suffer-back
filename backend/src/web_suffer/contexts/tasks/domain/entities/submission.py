from dataclasses import dataclass
from datetime import UTC, datetime

from web_suffer.contexts.tasks.domain.value_objects.submission_file import SubmissionFile
from web_suffer.contexts.tasks.domain.value_objects.submission_id import SubmissionID
from web_suffer.contexts.tasks.domain.value_objects.submission_status import SubmissionStatus
from web_suffer.contexts.tasks.domain.value_objects.task_id import TaskID
from web_suffer.shared.domain.value_objects.user_id import UserID
from web_suffer.shared.entities.base_entity import BaseEntity


@dataclass(slots=True)
class Submission(BaseEntity):
    """Доменная сущность задания (Entity DDD)."""

    _id: SubmissionID  # pyrefly: ignore [bad-override-mutable-attribute]
    _task_id: TaskID
    _user_id: UserID
    _content: str
    _file: SubmissionFile
    _status: SubmissionStatus
    _admin_comment: str

    @property
    def id(self) -> SubmissionID:
        """ID задания."""
        return self._id

    @property
    def user_id(self) -> UserID:
        """Пользователь."""
        return self._user_id

    @property
    def task_id(self) -> TaskID:
        """Задание."""
        return self._task_id

    @property
    def content(self) -> str:
        """Содержимое посылки."""
        return self._content

    @property
    def file(self) -> SubmissionFile:
        """Файл посылки."""
        return self._file

    @property
    def have_file(self) -> bool:
        """Содержится ли файл."""
        return self._file.does_have_file()

    @property
    def status(self) -> SubmissionStatus:
        """Статус отправления."""
        return self._status

    @property
    def admin_comment(self) -> str:
        """Комментарий проверяющего."""
        return self._admin_comment

    @BaseEntity.update
    def set_status(self, status: SubmissionStatus) -> None:
        """Обновление статуса."""
        self._status = status

    @BaseEntity.update
    def set_comment(self, admin_comment: str) -> None:
        """Обновление комментария проверяющего."""
        self._admin_comment = admin_comment

    @classmethod
    def create(
        cls,
        task_id: TaskID,
        user_id: UserID,
        content: str,
        file: SubmissionFile,
        status: SubmissionStatus | None = None,
        comment: str = "",
        id: SubmissionID | None = None,  # noqa: A002
    ) -> "Submission":
        """
        Фабричный метод создания новой посылки.

        Returns:
            Новая посылка.

        """
        now = datetime.now(UTC)
        return cls(
            _id=id or SubmissionID.new(),
            _created_at=now,
            _updated_at=now,
            _task_id=task_id,
            _user_id=user_id,
            _content=content,
            _file=file,
            _status=status or SubmissionStatus.PENDING,
            _admin_comment=comment,
        )

    @classmethod
    def hydrate(
        cls,
        id: SubmissionID,  # noqa: A002,
        created_at: datetime,
        updated_at: datetime,
        task_id: TaskID,
        user_id: UserID,
        content: str,
        file: SubmissionFile,
        status: SubmissionStatus,
        comment: str,
    ) -> "Submission":
        """
        Фабричный метод для восстановления задания из БД.

        Returns:
            Восстановленное из БД задание.

        """
        return cls(
            _id=id,
            _created_at=created_at,
            _updated_at=updated_at,
            _task_id=task_id,
            _user_id=user_id,
            _content=content,
            _file=file,
            _status=status,
            _admin_comment=comment,
        )
