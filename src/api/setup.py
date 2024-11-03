from typing import Any, Optional, Tuple

from fastapi import FastAPI

from src.api.common.middlewares import setup_global_middlewares
from src.api.common.responses import ORJSONResponse
from src.core.logger import log
from src.core.settings import Settings


def init_app(
    *sub_apps: Tuple[str, FastAPI, Optional[str]],
    settings: Settings,
    **kw: Any,
) -> FastAPI:
    log.info("Initialize General")
    app = FastAPI(
        default_response_class=ORJSONResponse,
        docs_url=None,
        redoc_url=None,
        swagger_ui_oauth2_redirect_url=None,
        **kw,
    )
    for apps in sub_apps:
        app.mount(*apps)

    setup_global_middlewares(app, settings)

    return app
