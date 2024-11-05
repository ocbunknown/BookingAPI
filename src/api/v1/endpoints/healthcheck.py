from fastapi import APIRouter, status

from src.common.dtos.base import DTO

healthcheck_router = APIRouter(
    prefix="/healthcheck",
    tags=["healthcheck"],
)


class OkStatus(DTO):
    status: str = "ok"


@healthcheck_router.get("", response_model=OkStatus, status_code=status.HTTP_200_OK)
async def get_status() -> OkStatus:
    return OkStatus()
