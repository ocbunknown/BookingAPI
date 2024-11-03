from fastapi import APIRouter, FastAPI

from .healthcheck import healthcheck_router
from .user import user_router

router = APIRouter()
router.include_router(user_router)
router.include_router(healthcheck_router)


def setup_routers(app: FastAPI) -> None:
    app.include_router(router)
