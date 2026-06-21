from uuid import UUID

from pydantic import BaseModel


class UserResponce(BaseModel):
    """
    Результат запроса получения информации о пользователе.

    user_id: ID пользователя.
    exp: опыт пользователя.
    money: деньги пользователя.

    """  # noqa: RUF002

    user_id: UUID
    exp: int
    money: int
