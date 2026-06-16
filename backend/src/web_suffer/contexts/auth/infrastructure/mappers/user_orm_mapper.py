from datetime import datetime

from sqlalchemy import ColumnElement

from web_suffer.contexts.auth.domain.entities.user import User
from web_suffer.contexts.auth.domain.value_objects import (
    PasswordHash,
    UserEmail,
    UserRole,
    UserStatus,
)
from web_suffer.contexts.auth.infrastructure.persistence.models.user_model import (
    UserORMModel,
)
from web_suffer.shared.domain.value_objects.user_id import UserID


class UserORMMapper:
    """Mapper между Domain Entity и ORM model."""

    @staticmethod
    def to_domain(orm: UserORMModel) -> User:
        """
        ORM Model -> Domain Entity.

        Returns:
            Пользователь из бд.

        """
        return User.hydrate(
            id=UserID(orm.id),
            email=UserEmail(orm.email),
            password_hash=PasswordHash(orm.password_hash),
            role=UserRole(orm.role),
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            status=UserStatus(orm.status),
        )

    @staticmethod
    def to_orm_partial(user: User) -> dict[str, str | datetime | ColumnElement[int]]:
        """
        Domain Entity -> Частичный ORM update.

        Returns:
            Частичный update ORM.

        """
        return {
            "email": user.email.value,
            "password_hash": user.password_hash.value,
            "role": user.role.value,
            "updated_at": user.updated_at,
            "status": str(user.status.value),
            "version": UserORMModel.version + 1,
        }

    @staticmethod
    def update_from_domain(
        orm: UserORMModel,
        user: User,
    ) -> None:
        """Обновление существующей ORM модели из Domain (без сохранения)."""
        orm.id = user.id.value
        orm.email = user.email.value
        orm.password_hash = user.password_hash.value
        orm.role = user.role.value
        orm.updated_at = user.updated_at
        orm.status = str(user.status.value)
