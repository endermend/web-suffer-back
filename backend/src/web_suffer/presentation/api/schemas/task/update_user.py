from uuid import UUID

from pydantic import BaseModel


class UpdateUserRequest(BaseModel):
    """
    Входные данные изменения пользователя.

    user_id: ID изменяемого пользователя.
    exp_diff: Разница опыта.
    money_diff: Разница монет.
    """

    user_id: UUID
    exp_diff: int
    money_diff: int
