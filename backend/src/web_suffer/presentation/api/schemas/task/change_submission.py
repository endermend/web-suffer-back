from uuid import UUID

from pydantic import BaseModel

from web_suffer.contexts.tasks.domain.types import SubmissionStatusType


class ChangeSubmissionRequest(BaseModel):
    """
    Входные данные изменения задания.

    status: "pending", "accepted" или "rejected".

    """

    submission_id: UUID
    status: SubmissionStatusType
    comment: str | None = None
