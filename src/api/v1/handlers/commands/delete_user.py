from typing import Any

from src.api.v1.handlers.base import BaseHandler
from src.common import dtos
from src.services.gateway import ServiceGateway


class DeleteUserHandler(BaseHandler[dtos.DeleteUser, dtos.User]):
    __slots__ = ("_gateway",)

    def __init__(self, gateway: ServiceGateway) -> None:
        self._gateway = gateway

    async def handle(self, query: dtos.DeleteUser, **kwargs: Any) -> dtos.User:
        async with self._gateway:
            return await self._gateway.user().delete(**query.model_dump(), **kwargs)
