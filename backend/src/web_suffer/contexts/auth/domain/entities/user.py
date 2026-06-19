from dataclasses import dataclass
from datetime import UTC, datetime

from web_suffer.contexts.auth.domain.value_objects import (
    PasswordHash,
    UserEmail,
)
from web_suffer.shared.domain.value_objects import UserID
from web_suffer.shared.domain.value_objects.user_role import UserRole
from web_suffer.shared.domain.value_objects.user_status import UserStatus
from web_suffer.shared.entities.base_entity import BaseEntity


@dataclass(slots=True)
class User(BaseEntity):
    """Доменная сущность пользователя (Entity DDD)."""

    _id: UserID  # pyrefly: ignore [bad-override-mutable-attribute]
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

    @BaseEntity.update
    def set_password_hash(self, password_hash: PasswordHash) -> None:
        """Обновление хеш пароля пользователя."""
        self._password_hash = password_hash

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
    def hydrate(
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
        Фабричный метод для восстановления пользователя из БД.

        Returns:
            Восстановленный из БД пользователь.

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
