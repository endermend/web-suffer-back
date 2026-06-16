from web_suffer.shared.domain.value_objects.user_id import UserID
from web_suffer.shared.entities.base_entity import BaseEntity


class UserT(BaseEntity):
    """Доменная сущность пользователя в заданиях (Entity DDD)."""

    _id: UserID
    _exp: int
    _money: int

    @property
    def id(self) -> UserID:
        """ID пользователя."""
        return self.__id

    @property
    def exp(self) -> int:
        """Опыт пользователя."""
        return self._exp

    @property
    def money(self) -> int:
        """Деньги пользователя."""
        return self._money

    @BaseEntity.update
    def set_money(self, money: int) -> None:
        """Обновленние денег пользователя."""
        self._money = money

    @BaseEntity.update
    def add_money(self, money: int) -> None:
        """Добавление денег пользователю."""
        self._money += money

    @BaseEntity.update
    def set_exp(self, exp: int) -> None:
        """Обновленние опыта пользователя."""
        self._money = exp

    @BaseEntity.update
    def add_exp(self, exp: int) -> None:
        """Добавление опыта пользователю."""
        self._money += exp

    @classmethod
    def create(
        cls,
        id: UserID,  # noqa: A002
        money: int = 0,
        exp: int = 0,
    ) -> "UserT":
        """
        Фабричный метод создания нового пользователя.

        Returns:
            Новый пользователь.

        """
        return cls(
            _id=id,
            _money=money,
            _exp=exp,
        )

    @classmethod
    def hydrate(
        cls,
        id: UserID,  # noqa: A002
        money: int = 0,
        exp: int = 0,
    ) -> "UserT":
        """
        Фабричный метод для восстановления пользователя из БД.

        Returns:
            Восстановленный из БД пользователь.

        """
        return cls(
            _id=id,
            _money=money,
            _exp=exp,
        )
