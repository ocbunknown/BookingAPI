from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Optional, Tuple

from fastapi import FastAPI

from src.api.common.exceptions import setup_exception_handlers
from src.api.common.responses import ORJSONResponse
from src.api.v1.di import setup_dependencies
from src.api.v1.endpoints import setup_routers
from src.api.v1.middlewares import setup_middlewares
from src.core.logger import log
from src.core.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    try:
        yield
    finally:
        if engine := app.state.get("engine", None):
            await engine.dispose()


def init_app_v1(
    settings: Settings,
    title: str = "FastAPI",
    version: str = "0.1.0",
    docs_url: Optional[str] = "/docs",
    redoc_url: Optional[str] = "/redoc",
    swagger_ui_oauth2_redirect_url: Optional[str] = "/docs/oauth2-redirect",
    **kw: Any,
) -> Tuple[str, FastAPI, Optional[str]]:
    log.info("Initialize V1 API")
    app = FastAPI(
        title=title,
        version=version,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
        docs_url=docs_url,
        redoc_url=redoc_url,
        swagger_ui_oauth2_redirect_url=swagger_ui_oauth2_redirect_url,
        **kw,
    )
    setup_dependencies(app, settings)
    setup_routers(app)
    setup_exception_handlers(app)
    setup_middlewares(app)

    return ("/api/v1", app, None)
