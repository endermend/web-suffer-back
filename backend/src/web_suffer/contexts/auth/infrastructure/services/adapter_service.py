from typing import override

from web_suffer.contexts.auth.application.mappers.auth_dto_mapper import IAuthDTOMapper
from web_suffer.contexts.auth.application.use_cases.get_userid import GetUserIDByAccessTokenUseCase
from web_suffer.contexts.auth.domain.repositories.user_repository import IUserRepository
from web_suffer.shared.application.dtos.access_token_dto import AccessTokenDTO
from web_suffer.shared.domain.interfaces.auth_service import IAuthService
from web_suffer.shared.domain.value_objects.user_id import UserID
from web_suffer.shared.domain.value_objects.user_right import UserRight


class AuthServiceAdapter(IAuthService):
    """Адаптер для сервиса аутентификации."""

    def __init__(
        self,
        get_user_id_use_case: GetUserIDByAccessTokenUseCase,
        user_repo: IUserRepository,
        mapper: IAuthDTOMapper,
    ) -> None:
        """Инициализация адаптера."""
        self._get_user_id_use_case = get_user_id_use_case
        self._user_repo = user_repo
        self._mapper = mapper

    @override
    async def get_user_id_by_token(self, acess_token: str) -> UserID:
        """
        Получить ID пользователя по токену через use case.

        Returns:
            ID пользователя по токену.

        """
        userid_dto = await self._get_user_id_use_case.execute(AccessTokenDTO(acess_token))
        return self._mapper.from_userid_dto(userid_dto)

    @override
    async def check_user_right(self, user_id: UserID, right: UserRight) -> bool:
        """
        Проверка прав пользователя по ID.

        Если указано неверное ID, возвращается False.

        Returns:
            true, если пользователь имеет право right.

        """
        user = await self._user_repo.get_user_by_id(user_id)
        return right.is_satisfied_by(user.role, user.status) if user else False
