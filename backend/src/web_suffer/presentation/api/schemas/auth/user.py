from uuid import UUID

from pydantic import BaseModel, EmailStr

from web_suffer.contexts.auth.domain.types import UserRolesType, UserStatusType


class UserResponse(BaseModel):
    """Схема данных ответа получения данных пользователя."""

    user_id: UUID
    email: EmailStr
    role: UserRolesType
    status: UserStatusType
