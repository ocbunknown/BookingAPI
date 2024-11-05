from fastapi import FastAPI
from starlette.middleware.errors import ServerErrorMiddleware

from .exceptions import handle_exception_middleware


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(ServerErrorMiddleware, handler=handle_exception_middleware)
