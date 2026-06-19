import shutil
import uuid
from pathlib import Path
from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, File, Form, Query, UploadFile, status

from web_suffer.contexts.tasks.application.dtos.submission_dto import ChangeSubmissionDTO, CreateSubmissionDTO, SubmissionIDDTO, SubmissionRangesDTO
from web_suffer.contexts.tasks.application.dtos.task_dto import UpdateTaskDTO
from web_suffer.contexts.tasks.application.dtos.usert_dto import UpdateUserTDTO
from web_suffer.contexts.tasks.application.use_cases.change_submission import ChangeSubmissionUseCase
from web_suffer.contexts.tasks.application.use_cases.create_submission import CreateSubmissionUseCase
from web_suffer.contexts.tasks.application.use_cases.get_submission_by_id import GetSubmissionByIDUseCase
from web_suffer.contexts.tasks.application.use_cases.get_submissions import GetSubmissionsUseCase
from web_suffer.contexts.tasks.application.use_cases.update_task import UpdateTaskUseCase
from web_suffer.contexts.tasks.application.use_cases.update_user import UpdateUserUseCase
from web_suffer.contexts.tasks.domain.types import SubmissionOrderBy, SubmissionStatus
from web_suffer.infrastructure.constants import UPLOAD_DIR
from web_suffer.presentation.api.routers.utils import CredentialsType
from web_suffer.presentation.api.schemas.submission import SubmissionResponce
from web_suffer.presentation.api.schemas.task.change_submission import ChangeSubmissionRequest
from web_suffer.presentation.api.schemas.task.update_task import UpdateTaskRequest, UpdateTaskResponse
from web_suffer.presentation.api.schemas.task.update_user import UpdateUserRequest

router = APIRouter(prefix="/task", tags=["Task"])


@router.post(
    "/change_submission",
    status_code=status.HTTP_200_OK,
    summary="Проверка отправления",
)
@inject
async def change_submission(
    credentials: CredentialsType,
    data: ChangeSubmissionRequest,
    use_case: FromDishka[ChangeSubmissionUseCase],
) -> None:
    """Эндпоинт проверки отправления."""
    access_token = credentials.credentials
    await use_case.execute(
        input_dto=ChangeSubmissionDTO(
            access_token=access_token,
            submission_id=data.submission_id,
            status=data.status,
            comment=data.comment or "",
        ),
    )


@router.post(
    "/create_submission",
    status_code=status.HTTP_200_OK,
    summary="Создание отправления",
)
@inject
async def create_submission(
    credentials: CredentialsType,
    task_id: Annotated[uuid.UUID, Form()],
    content: Annotated[str, Form()],
    use_case: FromDishka[CreateSubmissionUseCase],
    file: Annotated[UploadFile | None, File()] = None,
) -> None:
    """Эндпоинт создания отправления."""
    access_token = credentials.credentials
    file_path: Path | None = None
    if file is not None:
        file_name = uuid.uuid4()
        file_path = UPLOAD_DIR / f"{file_name}{Path(file.filename).suffix if file.filename is not None else ''}"

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    await use_case.execute(
        input_dto=CreateSubmissionDTO(
            access_token=access_token,
            task_id=task_id,
            content=content,
            file=file_path,
        ),
    )


@router.post(
    "/update_task",
    status_code=status.HTTP_200_OK,
    summary="Создание/изменение заданий",
)
@inject
async def update_task(
    credentials: CredentialsType,
    data: UpdateTaskRequest,
    use_case: FromDishka[UpdateTaskUseCase],
) -> UpdateTaskResponse:
    """
    Эндпоинт создания задания.

    Returns:
        ID нового/измененного задания.

    """
    access_token = credentials.credentials
    task_id = await use_case.execute(
        input_dto=UpdateTaskDTO(
            access_token=access_token,
            task_id=data.task_id,
            title=data.title,
            description=data.description,
            deadline=data.deadline,
            exp=data.exp,
            money=data.money,
        ),
    )
    return UpdateTaskResponse(
        task_id=task_id.task_id,
    )


@router.post(
    "/update_user",
    status_code=status.HTTP_200_OK,
    summary="Изменение пользователя.",
)
@inject
async def update_user(
    credentials: CredentialsType,
    data: UpdateUserRequest,
    use_case: FromDishka[UpdateUserUseCase],
) -> None:
    """Эндпоинт изменения пользователя."""
    access_token = credentials.credentials
    await use_case.execute(
        input_dto=UpdateUserTDTO(
            access_token=access_token,
            user_id=data.user_id,
            exp_diff=data.exp_diff,
            money_diff=data.money_diff,
        ),
    )


@router.get(
    "/submission",
    status_code=status.HTTP_200_OK,
    summary="Получение отправления",
)
@inject
async def submission(
    credentials: CredentialsType,
    submission_id: Annotated[uuid.UUID, Query(description="ID отправления")],
    use_case: FromDishka[GetSubmissionByIDUseCase],
) -> SubmissionResponce:
    """
    Эндпоинт получения отправления.

    Returns:
        SubmissionResponce

    """
    access_token = credentials.credentials
    output_dto = await use_case.execute(
        input_dto=SubmissionIDDTO(
            access_token=access_token,
            submission_id=submission_id,
        ),
    )
    return SubmissionResponce(
        submission_id=output_dto.submission_id,
        task_id=output_dto.task_id,
        user_id=output_dto.user_id,
        content=output_dto.content,
        file=output_dto.file.name if output_dto.file is not None else None,
        status=output_dto.status,
        comment=output_dto.comment,
    )


@router.get(
    "/submissions",
    status_code=status.HTTP_200_OK,
    summary="Получение отправлений по фильтру",
)
@inject
async def submissions(
    credentials: CredentialsType,
    use_case: FromDishka[GetSubmissionsUseCase],
    user_id: Annotated[uuid.UUID | None, Query(description="ID отправителя")] = None,
    status: Annotated[SubmissionStatus | None, Query(description="Статус отправления")] = None,
    order_by: Annotated[SubmissionOrderBy | None, Query(description="Призрак сортировки")] = None,
) -> list[SubmissionResponce]:
    """
    Эндпоинт получения отправлений по фильтру.

    Returns:
        Список отправлений.

    """
    access_token = credentials.credentials
    subms = await use_case.execute(
        input_dto=SubmissionRangesDTO(
            access_token=access_token,
            user_id=user_id,
            status=status,
            order_by=order_by,
        ),
    )
    return [SubmissionResponce(
        submission_id=subm.submission_id,
        task_id=subm.task_id,
        user_id=subm.user_id,
        content=subm.content,
        file=subm.file.name if subm.file is not None else None,
        status=subm.status,
        comment=subm.comment,
    )
    for subm in subms
    ]
