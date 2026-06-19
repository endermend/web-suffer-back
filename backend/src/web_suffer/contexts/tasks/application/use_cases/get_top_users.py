import structlog

from web_suffer.contexts.tasks.application.dtos.usert_dto import UserTDTO, UserTTOPDTO
from web_suffer.contexts.tasks.application.mappers.task_dto_mappers import ITaskDTOMapper
from web_suffer.contexts.tasks.domain.repository.user_repository import IUserTRepository

logger = structlog.stdlib.get_logger()


class GetTopUsersUseCase:
    """Use Case получения информации топ пользователей."""

    def __init__(
        self,
        user_repo: IUserTRepository,
        mapper: ITaskDTOMapper,
    ) -> None:
        """Инициализация use case."""
        self._user_repo = user_repo
        self._mapper = mapper

    async def execute(self, input_dto: UserTTOPDTO) -> list[UserTDTO]:
        """
        Получает информацию пользователей по id.

        Returns:
            list[UserTDTO]: информация пользователя.

        """
        users = await self._user_repo.get_list(amount=input_dto.amount, order_by="exp")

        return [self._mapper.to_user_dto(user=user) for user in users]
