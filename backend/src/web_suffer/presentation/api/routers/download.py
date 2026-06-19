from datetime import UTC, datetime, timedelta
from pathlib import Path

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from web_suffer.infrastructure.constants import UPLOAD_DIR

router = APIRouter(prefix="/download", tags=["Download"])


def is_safe_path(path: Path, base_dir: Path) -> bool:
    """
    Проверяет, находится ли путь внутри base_dir.

    Returns:
        true, если path находится внутри base_dir.

    """
    try:
        resolved_path = path.resolve()
        resolved_base = base_dir.resolve()

        return str(resolved_path).startswith(str(resolved_base))
    except (ValueError, OSError):
        return False


@router.get(
    "/{filename}",
    status_code=status.HTTP_200_OK,
    summary="Получение информации о пользователе по ID.",
)
async def download(filename: str) -> FileResponse:
    """
    Получение файла по названию.

    Returns:
        Сохраненный файл.

    Raises:
        HTTPException: если пытаются обмануть.

    """
    file_path = UPLOAD_DIR / filename

    if not is_safe_path(file_path, UPLOAD_DIR):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbiden")

    if not file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    if not file_path.is_file():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filename is not path")

    return FileResponse(
        path=file_path,
        filename=file_path.name,
        headers={
            "Cache-Control": "public, max-age=86400",  # 24 часа
            "Expires": (datetime.now(UTC) + timedelta(days=1)).strftime("%a, %d %b %Y %H:%M:%S GMT"),
            "ETag": f'"{file_path.stat().st_mtime}"',
        },
    )
