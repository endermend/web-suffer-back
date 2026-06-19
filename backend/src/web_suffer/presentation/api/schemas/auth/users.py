from uuid import UUID

from pydantic import BaseModel


class GetUsersResponse(BaseModel):
    """Схема данных ответа для получения списка пользователей."""

    user_id: UUID
