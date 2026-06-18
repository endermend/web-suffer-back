from web_suffer.contexts.auth.application.mappers.auth_dto_mapper import IAuthDTOMapper
from web_suffer.contexts.auth.application.use_cases.get_userid import GetUserIDByAccessTokenUseCase
from web_suffer.shared.application.dtos.access_token_dto import AccessTokenDTO
from web_suffer.shared.domain.interfaces.auth_service import IAuthService
from web_suffer.shared.domain.value_objects.user_id import UserID


class AuthServiceAdapter(IAuthService):
    """Адаптер для сервиса аутентификации."""

    def __init__(
            self,
            get_user_id_use_case: GetUserIDByAccessTokenUseCase,
            mapper: IAuthDTOMapper,
        ) -> None:
        """Инициализация адаптера."""
        self._get_user_id_use_case = get_user_id_use_case
        self._mapper = mapper

    async def get_user_id_by_token(self, acess_token: str) -> UserID:
        """
        Получить ID пользователя по токену через use case.

        Returns:
            ID пользователя по токену.

        """
        userid_dto = await self._get_user_id_use_case.execute(AccessTokenDTO(acess_token))
        return self._mapper.from_userid_dto(userid_dto)
