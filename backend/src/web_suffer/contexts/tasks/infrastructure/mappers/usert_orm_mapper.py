from web_suffer.contexts.tasks.domain.entities.user import UserT
from web_suffer.contexts.tasks.infrastructure.persistence.models.user_model import UserTORMModel
from web_suffer.shared.domain.value_objects.user_id import UserID


class UserTORMMapper:
    """Mapper между Domain Entity и ORM model."""

    @staticmethod
    def to_domain(orm: UserTORMModel) -> UserT:
        """
        ORM Model -> Domain Entity.

        Returns:
            Пользователь из бд.

        """
        return UserT.hydrate(
            id=UserID(orm.id),
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            money=orm.money,
            exp=orm.exp,
        )

    @staticmethod
    def update_from_domain(
        orm: UserTORMModel,
        user: UserT,
    ) -> None:
        """Обновление существующей ORM модели из Domain."""
        orm.id = user.id.value
        orm.updated_at = user.updated_at
        orm.money = user.money
        orm.exp = user.exp
