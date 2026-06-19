from uuid import UUID

from pydantic import BaseModel


class UserResponce(BaseModel):
    """
    Результат запроса получения задания.

    user_id: ID пользователя.
    exp: опыт пользователя.
    money: деньги пользователя.

    """

    user_id: UUID
    exp: int
    money: int
