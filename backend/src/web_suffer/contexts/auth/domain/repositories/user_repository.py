from abc import abstractmethod
from typing import Protocol

from web_suffer.contexts.auth.domain.entities import User
from web_suffer.contexts.auth.domain.value_objects import UserEmail
from web_suffer.shared.domain.value_objects import UserID


class IUserRepository(Protocol):
    """Протокол User репозитория."""

    @abstractmethod
    async def save(self, user: User) -> None:
        """Сохранение User."""

    @abstractmethod
    async def user_exists_by_email(self, email: UserEmail) -> bool:
        """Проверка существования User по UserEmail."""

    @abstractmethod
    async def get_user_by_email(self, email: UserEmail) -> User | None:
        """
        Получение User по UserEmail.

        None если пользователь не найден.
        """

    @abstractmethod
    async def get_user_by_id(self, user_id: UserID) -> User | None:
        """
        Получение User по UserId.

        Returns:
            Пользователь, если пользователь с таким ID существует, иначе None.

        """  # noqa: RUF002

    @abstractmethod
    async def get_users(self) -> list[User]:
        """
        Получение списка User с ролью user.

        Returns:
            Список пользователей или пустой список.

        """  # noqa: RUF002
