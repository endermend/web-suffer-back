from pydantic import BaseModel, EmailStr


class TopUserResponce(BaseModel):
    """
    Результат запроса получения информации о пользователе из топа.

    user_email: Email пользователя.
    exp: опыт пользователя.
    money: деньги пользователя.

    """  # noqa: RUF002

    user_email: EmailStr
    exp: int
    money: int
