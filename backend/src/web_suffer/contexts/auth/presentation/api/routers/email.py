from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from web_suffer.contexts.auth.application.dto.get_login import GetLoginInputDTO
from web_suffer.contexts.auth.application.use_cases import GetLoginUseCase
from web_suffer.contexts.auth.presentation.api.schemas.email import (
    GetEmailResponse,
)

router = APIRouter()


@router.get(
    "/email",
    status_code=status.HTTP_200_OK,
    summary="Получение почты",
)
@inject
async def email(
    access_token: str,
    use_case: FromDishka[GetLoginUseCase],
) -> GetEmailResponse:
    """
    Эндпоинт получения почты.

    Returns:
        GetEmailResponse

    """
    output_dto = await use_case.execute(
        input_dto=GetLoginInputDTO(access_token=access_token),
    )
    return GetEmailResponse(email=output_dto.email)
