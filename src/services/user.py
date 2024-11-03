from typing import Any, Optional

from src.common import dtos
from src.common.converters import (
    convert_user_model_to_delete_user_dto,
    convert_user_model_to_dto,
)
from src.common.exceptions import ConflictError, NotFoundError
from src.common.interfaces.hasher import AbstractHasher
from src.database.repositories.user import UserRepository
from src.services.service import Service


class UserService(Service[UserRepository]):
    __slots__ = ("reader", "writer")

    def __init__(self, repository: UserRepository, **kwargs: Any) -> None:
        super().__init__(repository, **kwargs)
        self.reader = repository.reader()
        self.writer = repository.writer()

    async def select_user(
        self,
        user_id: Optional[int] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> dtos.User:
        result = await self.reader.select(user_id, email, phone)
        if not result:
            raise NotFoundError("Not Found")

        return convert_user_model_to_dto(result)

    async def create_user(
        self, query: dtos.CreateUser, hasher: AbstractHasher
    ) -> dtos.User:
        query.password = hasher.hash_password(query.password)
        result = await self.writer.create(query)

        if not result:
            raise ConflictError("This user already exists")

        return convert_user_model_to_dto(result)

    async def delete_user(
        self,
        user_id: Optional[int] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> dtos.DeleteUser:
        result = await self.writer.delete(user_id, email, phone)
        if not result:
            raise NotFoundError("Not Found")

        return convert_user_model_to_delete_user_dto(result)

    async def update_user(
        self,
        query: dtos.UpdatePartial,
        hasher: AbstractHasher,
    ) -> dtos.User:
        if query.password:
            query.password = hasher.hash_password(query.password)

        result = await self.writer.update(**query.model_dump())
        if not result:
            raise NotFoundError("Not Found")

        return convert_user_model_to_dto(result)
