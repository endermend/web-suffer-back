from uuid import UUID

from pydantic import BaseModel

from web_suffer.contexts.tasks.domain.types import SubmissionStatus


class ChangeSubmissionRequest(BaseModel):
    """DTO изменения отправления."""

    submission_id: UUID
    status: SubmissionStatus
    comment: str | None
