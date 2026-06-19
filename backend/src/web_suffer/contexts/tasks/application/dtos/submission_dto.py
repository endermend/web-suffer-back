from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

from web_suffer.contexts.tasks.domain.types import SubmissionOrderBy, SubmissionStatus


@dataclass(slots=True, frozen=True)
class SubmissionDTO:
    """DTO отправления."""

    submission_id: UUID
    task_id: UUID
    user_id: UUID
    content: str
    file: Path | None
    status: SubmissionStatus
    comment: str


@dataclass(slots=True, frozen=True)
class SubmissionIDDTO:
    """DTO id отправления."""

    access_token: str
    submission_id: UUID


@dataclass(slots=True, frozen=True)
class CreateSubmissionDTO:
    """DTO создания отправления."""

    access_token: str
    task_id: UUID
    content: str
    file: Path | None


@dataclass(slots=True, frozen=True)
class ChangeSubmissionDTO:
    """DTO изменения отправления."""

    access_token: str
    submission_id: UUID
    status: SubmissionStatus
    comment: str


@dataclass(slots=True, frozen=True)
class SubmissionRangesDTO:
    """DTO получения списка отправлений."""

    access_token: str
    user_id: UUID | None
    status: SubmissionStatus | None
    order_by: SubmissionOrderBy | None
