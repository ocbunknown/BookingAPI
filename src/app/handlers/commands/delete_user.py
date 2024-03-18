from typing import Optional

from src.app.common import DTO, dto
from src.app.handlers.base import BaseHandler
from src.app.services.gateway import ServiceGateway


class DeleteUser(DTO):
    user_id: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class DeleteUserHandler(BaseHandler[DeleteUser, dto.User]):
    __slots__ = ("_gateway",)

    def __init__(self, gateway: ServiceGateway) -> None:
        self._gateway = gateway

    async def handle(self, query: DeleteUser) -> dto.DeleteUser:
        async with self._gateway:
            return await self._gateway.user().delete_user(**query.model_dump())
