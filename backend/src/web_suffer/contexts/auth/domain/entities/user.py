from dataclasses import dataclass
from datetime import UTC, datetime

from web_suffer.contexts.auth.domain.value_objects import (
    PasswordHash,
    UserEmail,
    UserRole,
    UserStatus,
)
from web_suffer.shared.domain.value_objects import UserID
from web_suffer.shared.entities.base_entity import BaseEntity


@dataclass(slots=True)
class User(BaseEntity):
    """Доменная сущность пользователя (Entity DDD)."""

    _id: UserID
    _email: UserEmail
    _password_hash: PasswordHash
    _role: UserRole
    _status: UserStatus = UserStatus.ACTIVE

    @property
    def id(self) -> UserID:
        """Id пользователя."""
        return self._id

    @property
    def email(self) -> UserEmail:
        """Email пользователя."""
        return self._email

    @property
    def password_hash(self) -> PasswordHash:
        """Хеш пароля пользователя."""
        return self._password_hash

    @property
    def role(self) -> UserRole:
        """Роль пользователя."""
        return self._role

    @property
    def status(self) -> UserStatus:
        """Статус пользователя."""
        return self._status

    @property
    def is_active(self) -> bool:
        """Активен ли пользователь."""
        return self._status.is_active()

    @BaseEntity.update
    def set_email(self, email: UserEmail) -> None:
        """Обновление почты пользователя."""
        self._email = email

    @BaseEntity.update
    def set_role(self, role: UserRole) -> None:
        """Обновление роли пользователя."""
        self._role = role

    @BaseEntity.update
    def set_status(self, status: UserStatus) -> None:
        """Обновление статуса пользователя."""
        self._status = status

    def __eq__(self, value: object) -> bool:
        """
        Сущности сравниваются по идентичности (DDD).

        Returns:
            Результат сравнения по self.id

        """
        if not isinstance(value, User):
            return NotImplemented
        return self.id == value.id

    def __hash__(self) -> int:
        """
        Сущности хэшируются по идентичности (DDD).

        Returns:
            Хеш по self.id

        """
        return hash(self.id)

    @classmethod
    def register(
        cls,
        email: UserEmail,
        password_hash: PasswordHash,
        role: UserRole,
        id: UserID | None = None,  # noqa: A002
    ) -> "User":
        """
        Фабричный метод для регистрации пользователя по почте, паролю и роли.

        Returns:
            Новый пользователь.

        """
        now = datetime.now(UTC)
        return cls(
            _id=id if id is not None else UserID.new(),
            _email=email,
            _password_hash=password_hash,
            _role=role,
            _created_at=now,
            _updated_at=now,
            _status=UserStatus.ACTIVE,
        )

    @classmethod
    def hydrate(  # noqa: PLR0913, PLR0917
        cls,
        id: UserID,  # noqa: A002
        email: UserEmail,
        password_hash: PasswordHash,
        role: UserRole,
        created_at: datetime,
        updated_at: datetime,
        status: UserStatus,
    ) -> "User":
        """
        Фабричный метод для востановления пользователя из БД.

        Returns:
            Востановленный из БД пользователь.

        """
        return cls(
            _id=id,
            _email=email,
            _password_hash=password_hash,
            _role=role,
            _created_at=created_at,
            _updated_at=updated_at,
            _status=status,
        )
