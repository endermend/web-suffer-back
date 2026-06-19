from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Cookie, HTTPException, Response, status

from web_suffer.contexts.auth.application.dtos.token_dto import RefreshTokenDTO
from web_suffer.contexts.auth.application.dtos.user_dto import CredentialsDTO, UpdateUserDTO
from web_suffer.contexts.auth.application.use_cases import (
    GetLoginByAccessTokenUseCase,
    GetUsersUseCase,
    LoginUserUseCase,
    RefreshUserUseCase,
    RegisterUserUseCase,
    UpdateUserUseCase,
)
from web_suffer.contexts.auth.domain.types import UserRolesType, UserStatusType
from web_suffer.contexts.auth.infrastructure.services.cookie_service import CookieService
from web_suffer.infrastructure.constants import REFRESH_TOKEN_COOKIE_NAME
from web_suffer.presentation.api.adapters.fastapi_response_adapter import FastAPIResponseAdapter
from web_suffer.presentation.api.routers.utils import CredentialsType
from web_suffer.presentation.api.schemas.auth.email import GetEmailResponse
from web_suffer.presentation.api.schemas.auth.login import (
    UserLoginRequest,
    UserLoginResponse,
)
from web_suffer.presentation.api.schemas.auth.refresh import (
    UserRefreshResponse,
)
from web_suffer.presentation.api.schemas.auth.register import (
    UserRegisterRequest,
    UserRegisterResponse,
)
from web_suffer.presentation.api.schemas.auth.users import GetUsersResponse
from web_suffer.shared.application.dtos.access_token_dto import AccessTokenDTO

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Вход в аккаунт",
)
@inject
async def login(
    response: Response,
    data: UserLoginRequest,
    use_case: FromDishka[LoginUserUseCase],
    cookie_service: FromDishka[CookieService],
) -> UserLoginResponse:
    """
    Эндпоинт входа в аккаунт.

    Returns:
        UserLoginResponse

    """
    output_dto = await use_case.execute(
        input_dto=CredentialsDTO(email=data.email, password=data.password),
    )
    wrapper = FastAPIResponseAdapter(response)
    cookie_service.set_refresh_token(response=wrapper, token=output_dto.refresh_token)
    return UserLoginResponse(access_token=output_dto.access_token)


@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    summary="Получение новой пары токенов",
)
@inject
async def refresh(
    response: Response,
    use_case: FromDishka[RefreshUserUseCase],
    cookie_service: FromDishka[CookieService],
    refresh_token: Annotated[
        str | None,
        Cookie(alias=REFRESH_TOKEN_COOKIE_NAME),
    ] = None,
) -> UserRefreshResponse:
    """
    Эндпоинт обновления токенов.

    Returns:
        UserRefreshResponse

    Raises:
        HTTPException: refresh token отсутствует в куки

    """
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )

    output_dto = await use_case.execute(
        input_dto=RefreshTokenDTO(refresh_token=refresh_token),
    )

    wrapper = FastAPIResponseAdapter(response)
    cookie_service.set_refresh_token(response=wrapper, token=output_dto.refresh_token)

    return UserRefreshResponse(access_token=output_dto.access_token)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация пользователя",
)
@inject
async def register(
    response: Response,
    data: UserRegisterRequest,
    use_case: FromDishka[RegisterUserUseCase],
    cookie_service: FromDishka[CookieService],
) -> UserRegisterResponse:
    """
    Эндпоинт регистрации.

    Returns:
        UserRegisterResponse

    """
    output_dto = await use_case.execute(
        input_dto=CredentialsDTO(email=data.email, password=data.password),
    )

    wrapper = FastAPIResponseAdapter(response)
    cookie_service.set_refresh_token(response=wrapper, token=output_dto.refresh_token)

    return UserRegisterResponse(access_token=output_dto.access_token)


@router.post(
    "/update-user",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Изменение данных пользователя",
)
@inject
async def update_user(
    credentials: CredentialsType,
    use_case: FromDishka[UpdateUserUseCase],
    user_id: UUID | None = None,
    email: str | None = None,
    role: UserRolesType | None = None,
    status: UserStatusType | None = None,
    new_password: str | None = None,
) -> None:
    """Эндпоинт изменение данных пользователя."""
    access_token = credentials.credentials
    await use_case.execute(
        input_dto=UpdateUserDTO(
            access_token=access_token,
            user_id=user_id,
            email=email,
            role=role,
            status=status,
            new_password=new_password,
        ),
    )


@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    summary="Получение списка пользователей",
)
@inject
async def users(
    credentials: CredentialsType,
    use_case: FromDishka[GetUsersUseCase],
) -> list[GetUsersResponse]:
    """
    Эндпоинт получения списка пользователей.

    Returns:
        GetEmailResponse

    """
    access_token = credentials.credentials
    output_dto = await use_case.execute(
        input_dto=AccessTokenDTO(access_token=access_token),
    )
    return [GetUsersResponse(email=user.email) for user in output_dto]


@router.get(
    "/email",
    status_code=status.HTTP_200_OK,
    summary="Получение почты",
)
@inject
async def email(
    credentials: CredentialsType,
    use_case: FromDishka[GetLoginByAccessTokenUseCase],
) -> GetEmailResponse:
    """
    Эндпоинт получения почты.

    Returns:
        GetEmailResponse

    """
    access_token = credentials.credentials
    output_dto = await use_case.execute(
        input_dto=AccessTokenDTO(access_token=access_token),
    )
    return GetEmailResponse(email=output_dto.email)
