from typing import Any

from src.api.v1.handlers.base import BaseHandler
from src.common import DTO, dtos
from src.services.gateway import ServiceGateway


class GetUser(DTO):
    user_id: int


class GetUserHandler(BaseHandler[GetUser, dtos.User]):
    __slots__ = ("_gateway",)

    def __init__(self, gateway: ServiceGateway) -> None:
        self._gateway = gateway

    async def handle(self, query: GetUser, **kwargs: Any) -> dtos.User:
        async with self._gateway:
            return await self._gateway.user().select_user(
                **query.model_dump(), **kwargs
            )
