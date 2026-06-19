
import shutil
import uuid
from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, File, Path, UploadFile, status

from web_suffer.contexts.tasks.application.dtos.submission_dto import ChangeSubmissionDTO, CreateSubmissionDTO
from web_suffer.contexts.tasks.application.use_cases.change_submission import ChangeSubmissionUseCase
from web_suffer.contexts.tasks.application.use_cases.create_submission import CreateSubmissionUseCase
from web_suffer.presentation.api.routers.utils import CredentialsType
from web_suffer.presentation.api.schemas.task.change_submission import ChangeSubmissionRequest
from web_suffer.presentation.api.schemas.task.create_submission import CreateSubmissionRequest

UPLOAD_DIR = Path("./files")


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


@router.post(
    "/create_submission",
    status_code=status.HTTP_200_OK,
    summary="Создание задания",
)
@inject
async def create_submission(
    credentials: CredentialsType,
    data: CreateSubmissionRequest,
    use_case: FromDishka[CreateSubmissionUseCase],
    file: Annotated[UploadFile, File()],
) -> None:
    """Эндпоинт создания задания."""
    access_token = credentials.credentials
    file_name = uuid.uuid4()
    file_path = UPLOAD_DIR / f"{file_name}{Path(file.filename).suffix}"

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    await use_case.execute(
        input_dto=CreateSubmissionDTO(
            access_token=access_token,
            task_id=data.task_id,
            content=data.content,
            file=file_path,
        ),
    )
