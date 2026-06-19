import shutil
import uuid
from pathlib import Path
from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, File, Form, UploadFile, status

from web_suffer.contexts.tasks.application.dtos.submission_dto import ChangeSubmissionDTO, CreateSubmissionDTO
from web_suffer.contexts.tasks.application.dtos.task_dto import UpdateTaskDTO
from web_suffer.contexts.tasks.application.use_cases.change_submission import ChangeSubmissionUseCase
from web_suffer.contexts.tasks.application.use_cases.create_submission import CreateSubmissionUseCase
from web_suffer.contexts.tasks.application.use_cases.update_task import UpdateTaskUseCase
from web_suffer.presentation.api.routers.utils import CredentialsType
from web_suffer.presentation.api.schemas.task.change_submission import ChangeSubmissionRequest
from web_suffer.presentation.api.schemas.task.update_task import UpdateTaskRequest, UpdateTaskResponse

UPLOAD_DIR = Path("./files")


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
        task_id=task_id,
    )
