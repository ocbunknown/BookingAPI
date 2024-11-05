from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import ColumnExpressionArgument

from src.database import models
from src.database.exceptions import InvalidParamsError
from src.database.repositories.base import BaseInteractor

if TYPE_CHECKING:
    from src.common import dtos


class UserWriter(BaseInteractor[models.User]):
    __slots__ = ()

    async def create(self, query: dtos.CreateUser) -> Optional[models.User]:
        return await self.repository._crud.insert(**query.model_dump())

    async def update(
        self,
        data: dtos.UpdateUser,
        user_id: Optional[int] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> Optional[models.User]:
        if not any([user_id, email, phone]):
            raise InvalidParamsError("at least one identifier must be provided")

        where_clauses: list[ColumnExpressionArgument[bool]] = []

        if user_id:
            where_clauses.append(self.repository.model.id == user_id)
        if email:
            where_clauses.append(self.repository.model.email == email)
        if phone:
            where_clauses.append(self.repository.model.phone == phone)

        result = await self.repository._crud.update(
            *where_clauses, **data.model_dump(exclude_none=True)
        )
        return result[0] if result else None

    async def delete(
        self,
        user_id: Optional[int] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> Optional[models.User]:
        if not any([user_id, email, phone]):
            raise InvalidParamsError("at least one identifier must be provided")

        where_clauses: list[ColumnExpressionArgument[bool]] = []

        if user_id:
            where_clauses.append(self.repository.model.id == user_id)
        if email:
            where_clauses.append(self.repository.model.email == email)
        if phone:
            where_clauses.append(self.repository.model.phone == phone)

        result = await self.repository._crud.delete(*where_clauses)
        return result[0] if result else None
