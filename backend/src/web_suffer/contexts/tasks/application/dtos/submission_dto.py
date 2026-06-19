from dataclasses import dataclass
from pathlib import Path
from uuid import UUID


@dataclass(slots=True, frozen=True)
class SubmissionDTO:
    """DTO отправления."""

    submission_id: UUID
    task_id: UUID
    user_id: UUID
    content: str
    file: Path | None
    status: str
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
    status: str
    comment: str
