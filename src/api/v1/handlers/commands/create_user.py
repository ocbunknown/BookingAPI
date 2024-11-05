from typing import Any

from src.api.v1.handlers.base import BaseHandler
from src.common import dtos
from src.common.interfaces.hasher import AbstractHasher
from src.services.gateway import ServiceGateway


class CreateUserHandler(BaseHandler[dtos.CreateUser, dtos.User]):
    __slots__ = ("_gateway",)

    def __init__(self, gateway: ServiceGateway, hasher: AbstractHasher) -> None:
        self._gateway = gateway
        self.hasher = hasher

    async def handle(self, query: dtos.CreateUser, **kwargs: Any) -> dtos.User:
        async with self._gateway:
            return await self._gateway.user().create(
                query=query, hasher=self.hasher, **kwargs
            )
