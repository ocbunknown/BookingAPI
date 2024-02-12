from fastapi import FastAPI

from src.main.routers import init_routers


def create_app() -> FastAPI:
    app = FastAPI()
    init_routers(app)
    return app
