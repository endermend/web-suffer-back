from dataclasses import dataclass
from datetime import UTC, datetime

from web_suffer.contexts.tasks.domain.value_objects.task_id import TaskID
from web_suffer.shared.entities.base_entity import BaseEntity


@dataclass(slots=True)
class Task(BaseEntity):
    """Доменная сущность задания (Entity DDD)."""

    _id: TaskID
    _title: str
    _description: str
    _deadline: datetime
    _exp: int
    _money: int

    @property
    def id(self) -> TaskID:
        """ID задания."""
        return self._id

    @property
    def title(self) -> str:
        """Название задания."""
        return self._title

    @property
    def description(self) -> str:
        """Описание задания."""
        return self._description

    @property
    def deadline(self) -> datetime:
        """Дедлайн задания."""
        return self._deadline

    @property
    def exp(self) -> int:
        """Опыт за задание."""
        return self._exp

    @property
    def money(self) -> int:
        """Денежная награда за задание."""
        return self._money

    @BaseEntity.update
    def set_title(self, title: str) -> None:
        """Обновление названия."""
        self._title = title

    @BaseEntity.update
    def set_description(self, description: str) -> None:
        """Обновление описания."""
        self._description = description

    @BaseEntity.update
    def set_deadline(self, deadline: datetime) -> None:
        """Обновление дедлайна."""
        self._deadline = deadline

    @BaseEntity.update
    def set_exp(self, exp: int) -> None:
        """Обновление опыта за задание."""
        self._exp = exp

    @BaseEntity.update
    def set_money(self, money: int) -> None:
        """Обновление денежной награды."""
        self._money = money

    @classmethod
    def create(
        cls,
        title: str,
        description: str,
        deadline: datetime,
        exp: int,
        money: int,
        id: TaskID | None = None,  # noqa: A002
    ) -> "Task":
        """
        Фабричный метод создания нового задания.

        Returns:
            Новое задание.

        """
        now = datetime.now(UTC)
        return cls(
            _id=id or TaskID.new(),
            _created_at=now,
            _updated_at=now,
            _title=title,
            _description=description,
            _deadline=deadline,
            _exp=exp,
            _money=money,
        )

    @classmethod
    def hydrate(
        cls,
        id: TaskID,  # noqa: A002
        created_at: datetime,
        updated_at: datetime,
        title: str,
        description: str,
        deadline: datetime,
        exp: int,
        money: int,
    ) -> "Task":
        """
        Фабричный метод для восстановления задания из БД.

        Returns:
            Восстановленное из БД задание.

        """
        return cls(
            _id=id,
            _created_at=created_at,
            _updated_at=updated_at,
            _title=title,
            _description=description,
            _deadline=deadline,
            _exp=exp,
            _money=money,
        )
