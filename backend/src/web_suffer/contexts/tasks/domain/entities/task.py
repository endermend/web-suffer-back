from datetime import datetime

from web_suffer.contexts.tasks.domain.value_objects.task_id import TaskID
from web_suffer.shared.entities.base_entity import BaseEntity


class Task(BaseEntity):
    """Доменная сущность задания (Entity DDD)."""

    _id: TaskID
    _title: str
    _description: str
    _deadline: datetime

    @property
    def id(self) -> TaskID:
        """ID задания."""
        return self._id

    @property
    def title(self) -> str:
        """Название задания."""
        return self._email

    @property
    def description(self) -> str:
        """Описание задания."""
        return self._description

    @property
    def deadline(self) -> datetime:
        """Дедлайн задания."""
        return self._deadline

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
