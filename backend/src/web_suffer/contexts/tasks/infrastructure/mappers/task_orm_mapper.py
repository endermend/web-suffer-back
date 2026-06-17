

from web_suffer.contexts.tasks.domain.entities.task import Task
from web_suffer.contexts.tasks.domain.value_objects.task_id import TaskID
from web_suffer.contexts.tasks.infrastructure.persistence.models.task_model import TaskORMModel


class TaskORMMapper:
    """Mapper между Domain Entity и ORM model."""

    @staticmethod
    def to_domain(orm: TaskORMModel) -> Task:
        """
        ORM Model -> Domain Entity.

        Returns:
            Отправление из бд.

        """
        return Task.hydrate(
            id=TaskID(orm.id),
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            title=orm.title,
            description=orm.description,
            deadline=orm.deadline,
            exp=orm.exp,
            money=orm.money,
        )

    @staticmethod
    def update_from_domain(
        orm: TaskORMModel,
        entity: Task,
    ) -> None:
        """Обновление существующей ORM модели из Domain."""
        orm.id = entity.id.value
        orm.updated_at = entity.updated_at
        orm.title = entity.title
        orm.description = entity.description
        orm.deadline = entity.deadline
        orm.exp = entity.exp
        orm.money = entity.money
