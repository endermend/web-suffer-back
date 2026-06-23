from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import UUID

from web_suffer.contexts.tasks.domain.types import SubmissionOrderByType, SubmissionStatusType


@dataclass(slots=True, frozen=True)
class SubmissionDTO:
    """DTO отправления."""

    submission_id: UUID
    task_id: UUID
    user_id: UUID
    content: str
    file: Path | None
    status: SubmissionStatusType
    comment: str


@dataclass(slots=True, frozen=True)
class SubmissionTokenIDDTO:
    """DTO id отправления."""

    access_token: str
    submission_id: UUID


@dataclass(slots=True, frozen=True)
class SubmissionIDDTO:
    """DTO id отправления."""

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
    status: SubmissionStatusType
    comment: str


@dataclass(slots=True, frozen=True)
class SubmissionRangesDTO:
    """DTO получения списка отправлений."""

    access_token: str
    user_id: UUID | None
    status: SubmissionStatusType | None
    updated_after: datetime | None
    order_by: SubmissionOrderByType | None
