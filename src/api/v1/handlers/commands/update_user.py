from typing import Any, Optional

from src.api.v1.handlers.base import BaseHandler
from src.common import DTO, dtos
from src.services.gateway import ServiceGateway


class UpdateUser(DTO):
    id: int
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class UpdateUserHandler(BaseHandler[UpdateUser, dtos.User]):
    __slots__ = ("_gateway",)

    def __init__(self, gateway: ServiceGateway) -> None:
        self._gateway = gateway

    async def handle(self, query: UpdateUser, **kwargs: Any) -> dtos.User:
        async with self._gateway:
            return await self._gateway.user().update_user(query, **kwargs)  # type: ignore[arg-type]
