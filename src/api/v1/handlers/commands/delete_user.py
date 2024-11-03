from typing import Any, Optional

from src.api.v1.handlers.base import BaseHandler
from src.common import DTO, dtos
from src.services.gateway import ServiceGateway


class DeleteUser(DTO):
    user_id: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class DeleteUserHandler(BaseHandler[DeleteUser, dtos.DeleteUser]):
    __slots__ = ("_gateway",)

    def __init__(self, gateway: ServiceGateway) -> None:
        self._gateway = gateway

    async def handle(self, query: DeleteUser, **kwargs: Any) -> dtos.DeleteUser:
        async with self._gateway:
            return await self._gateway.user().delete_user(
                **query.model_dump(), **kwargs
            )
