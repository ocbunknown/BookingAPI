from typing import Any, Optional

from src.api.v1.handlers.base import BaseHandler
from src.common import DTO, dtos
from src.common.interfaces.hasher import AbstractHasher
from src.services.gateway import ServiceGateway


class CreateUser(DTO):
    email: Optional[str] = None
    phone: str
    password: str


class CreateUserHandler(BaseHandler[CreateUser, dtos.User]):
    __slots__ = ("_gateway",)

    def __init__(self, gateway: ServiceGateway, hasher: AbstractHasher) -> None:
        self._gateway = gateway
        self.hasher = hasher

    async def handle(self, query: CreateUser, **kwargs: Any) -> dtos.User:
        async with self._gateway:
            return await self._gateway.user().create_user(query, self.hasher, **kwargs)  # type: ignore[arg-type]
