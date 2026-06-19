from uuid import UUID

from pydantic import BaseModel

from web_suffer.contexts.tasks.domain.types import SubmissionStatus


class ChangeSubmissionRequest(BaseModel):
    """
    Входные данные изменения задания.

    status: "pending", "accepted" или "rejected".

    """

    submission_id: UUID
    status: SubmissionStatus
    comment: str | None = None
