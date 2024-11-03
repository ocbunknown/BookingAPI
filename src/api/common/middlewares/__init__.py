from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.core.settings import Settings

from .context import set_request_id_middleware


def setup_global_middlewares(app: FastAPI, settings: Settings) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.server.origins,
        allow_credentials=True,
        allow_methods=settings.server.methods,
        allow_headers=settings.server.headers,
    )
    app.add_middleware(BaseHTTPMiddleware, dispatch=set_request_id_middleware)
