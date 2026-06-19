
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from web_suffer.contexts.tasks.application.dtos.submission_dto import ChangeSubmissionDTO
from web_suffer.contexts.tasks.application.use_cases.change_submission import ChangeSubmissionUseCase
from web_suffer.presentation.api.routers.utils import CredentialsType
from web_suffer.presentation.api.schemas.task.change_submission import ChangeSubmissionRequest

router = APIRouter(prefix="/task", tags=["Task"])


@router.post(
    "/change_submission",
    status_code=status.HTTP_200_OK,
    summary="Проверка задания",
)
@inject
async def change_submission(
    credentials: CredentialsType,
    data: ChangeSubmissionRequest,
    use_case: FromDishka[ChangeSubmissionUseCase],
) -> None:
    """Эндпоинт проверки задания."""
    access_token = credentials.credentials
    await use_case.execute(
        input_dto=ChangeSubmissionDTO(
            access_token=access_token,
            submission_id=data.submission_id,
            status=data.status,
            comment=data.comment or "",
        ),
    )
