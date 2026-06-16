import logging

from web_suffer.contexts.auth.application.interfaces.password_hasher import IPasswordHasher
from web_suffer.contexts.auth.domain.entities import User
from web_suffer.contexts.auth.domain.repositories import IUserRepository
from web_suffer.contexts.auth.domain.value_objects import UserEmail, UserRole
from web_suffer.contexts.auth.domain.value_objects.password_hash import PasswordHash
from web_suffer.infrastructure.config import Config

logger = logging.getLogger(__name__)


class SuperAdminSeeder:
    """Создание супер админа при первом запуске."""

    def __init__(
        self,
        user_repo: IUserRepository,
        password_hasher: IPasswordHasher,
        config: Config,
    ) -> None:
        """Инициализация SuperAdminSeeder."""
        self._user_repo = user_repo
        self._password_hasher = password_hasher
        self._config = config

    async def seed(self) -> None:
        """Добавление админа в БД."""
        email = UserEmail(self._config.SUPERADMIN.EMAIL)

        if await self._user_repo.user_exists_by_email(email):
            logger.info("Superadmin уже есть.")
            return

        password_hash = PasswordHash(self._password_hasher.hash_password(self._config.SUPERADMIN.PASSWORD))
        superadmin = User.register(
            email=email,
            password_hash=password_hash,
            role=UserRole.ADMIN,
        )
        await self._user_repo.save(superadmin)
        logger.info("Superadmin создан")
