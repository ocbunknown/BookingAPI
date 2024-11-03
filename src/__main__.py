from src.api.setup import init_app
from src.api.v1.setup import init_app_v1
from src.core.settings import PROJECT_NAME, PROJECT_VERSION, load_settings
from src.core.uvicorn_server import run_api_uvicorn


def main() -> None:
    settings = load_settings()
    app = init_app(
        init_app_v1(settings, title=PROJECT_NAME, version=PROJECT_VERSION),
        settings=settings,
    )

    run_api_uvicorn(app, settings)


if __name__ == "__main__":
    main()
