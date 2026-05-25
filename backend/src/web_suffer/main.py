import uvicorn

from web_suffer.infrastructure.config import Config
from web_suffer.infrastructure.log_config import setup_logging


def main() -> None:
    """Запуск FastAPI приложения в помощью uvicorn."""
    config = Config()
    setup_logging(env=config.APP.ENV)

    uvicorn.run(
        "web_suffer.presentation.api.app_factory:create_app",
        factory=True,
        host="0.0.0.0",  # noqa: S104
        port=config.APP.PORT,
        log_config=None,
        access_log=config.APP.ENV == "dev",
    )


if __name__ == "__main__":
    main()
