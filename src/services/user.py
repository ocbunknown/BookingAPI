from typing import Any, Optional

from src.common import dtos
from src.common.exceptions import ConflictError, NotFoundError
from src.common.interfaces.hasher import AbstractHasher
from src.database.converter import from_model_to_dto
from src.database.repositories.user import UserRepository
from src.database.tools import on_integrity
from src.services.service import Service


class UserService(Service[UserRepository]):
    __slots__ = ("reader", "writer")

    def __init__(self, repository: UserRepository, **kwargs: Any) -> None:
        super().__init__(repository, **kwargs)
        self.reader = repository.reader()
        self.writer = repository.writer()

    async def select(
        self,
        user_id: Optional[int] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> dtos.User:
        result = await self.reader.select(user_id, email, phone)
        if not result:
            raise NotFoundError("User not found")

        return from_model_to_dto(result, dtos.User)

    @on_integrity("email", "phone")
    async def create(self, query: dtos.CreateUser, hasher: AbstractHasher) -> dtos.User:
        query.password = hasher.hash_password(query.password)
        result = await self.writer.create(query)

        if not result:
            raise ConflictError("This user already exists")

        return from_model_to_dto(result, dtos.User)

    async def delete(
        self,
        user_id: Optional[int] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> dtos.User:
        result = await self.writer.delete(user_id, email, phone)
        if not result:
            raise ConflictError("Cannot delete user")

        return from_model_to_dto(result, dtos.User)

    async def update(
        self,
        hasher: AbstractHasher,
        data: dtos.UpdateUserQuery,
    ) -> dtos.User:
        if data.password:
            data.password = hasher.hash_password(data.password)

        result = await self.writer.update(
            user_id=data.user_id,
            email=data.email,
            phone=data.phone,
            data=dtos.UpdateUser(**data.model_dump()),
        )
        if not result:
            raise ConflictError("Cannot update user")

        return from_model_to_dto(result, dtos.User)
