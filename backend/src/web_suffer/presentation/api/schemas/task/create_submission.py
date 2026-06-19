from uuid import UUID

from pydantic import BaseModel


class CreateSubmissionRequest(BaseModel):
    """DTO изменения отправления."""

    task_id: UUID
    content: str
