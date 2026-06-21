import structlog

from web_suffer.contexts.auth.application.dtos.user_dto import UserDTO
from web_suffer.contexts.auth.application.mappers.auth_dto_mapper import (
    IAuthDTOMapper,
)
from web_suffer.contexts.auth.domain.repositories import IUserRepository
from web_suffer.shared.application.dtos.user_id_dto import UserIDDTO

logger = structlog.stdlib.get_logger()


class GetUsersByIDUseCase:
    """Use case получения списка пользователей по списку id."""

    def __init__(
        self,
        user_repo: IUserRepository,
        mapper: IAuthDTOMapper,
    ) -> None:
        """Инициализирует use case получения логина по access-токену."""
        self._user_repo = user_repo
        self._mapper = mapper

    async def execute(self, input_dto: list[UserIDDTO]) -> list[UserDTO]:
        """
        Возвращает данные пользователей.

        Returns:
            DTO с данными пользователей.

        Raises:
            ValueError: одного или несколько пользователей не существует.

        """  # noqa: RUF002
        users = await self._user_repo.get_users_by_id(
            users_id=[self._mapper.from_userid_dto(user_id) for user_id in input_dto],
        )

        if len(users) != len(input_dto):
            logger.warning("auth.users.failed", reason="users_not_found")
            raise ValueError

        return [self._mapper.to_user_dto(user) for user in users]
