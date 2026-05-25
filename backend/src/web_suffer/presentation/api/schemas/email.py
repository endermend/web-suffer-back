from pydantic import BaseModel, EmailStr


class GetEmailRequest(BaseModel):
    """Схема данных запроса для входа в аккаунт."""

    access_token: str


class GetEmailResponse(BaseModel):
    """Схема данных ответа для входа в аккаунт."""

    email: EmailStr
