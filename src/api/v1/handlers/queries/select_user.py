from typing import Any

from src.api.v1.handlers.base import BaseHandler
from src.common import dtos
from src.services.gateway import ServiceGateway


class GetUserHandler(BaseHandler[dtos.SelectUser, dtos.User]):
    __slots__ = ("_gateway",)

    def __init__(self, gateway: ServiceGateway) -> None:
        self._gateway = gateway

    async def handle(self, query: dtos.SelectUser, **kwargs: Any) -> dtos.User:
        async with self._gateway.database.manager.session:
            return await self._gateway.user().select(**query.model_dump(), **kwargs)
