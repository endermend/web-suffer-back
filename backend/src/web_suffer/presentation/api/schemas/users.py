from pydantic import BaseModel, EmailStr


class GetUsersResponse(BaseModel):
    """Схема данных ответа для получения списка пользователей."""

    email: EmailStr
