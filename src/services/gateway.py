from src.common.interfaces.gateway import BaseGateway
from src.database import DBGateway
from src.services.user import UserService


class ServiceGateway(BaseGateway):
    __slots__ = ("database",)

    def __init__(self, database: DBGateway) -> None:
        self.database = database
        super().__init__(database)

    def user(self) -> UserService:
        return UserService(self.database.user())
