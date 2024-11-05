from typing import Any

import uvicorn

from src.core.logger import LOG_LEVEL, log
from src.core.settings import Settings


def run_api_uvicorn(app: Any, config: Settings, **kw: Any) -> None:
    uv_config = uvicorn.Config(
        app,
        host=config.server.host,
        port=config.server.port,
        log_level=LOG_LEVEL.lower(),
        server_header=False,
        **kw,
    )
    server = uvicorn.Server(uv_config)
    log.info("Running API Uvicorn")
    server.run()
