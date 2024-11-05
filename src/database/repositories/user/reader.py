from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import ColumnExpressionArgument

from src.database import models
from src.database.exceptions import InvalidParamsError
from src.database.repositories.base import BaseInteractor


class UserReader(BaseInteractor[models.User]):
    __slots__ = ()

    async def select(
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

        return await self.repository._crud.select(*where_clauses)

    async def select_many(
        self,
        user_id: Optional[int] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
    ) -> Sequence[models.User]:
        if not any([user_id, email, phone]):
            raise InvalidParamsError("at least one identifier must be provided")

        where_clauses: list[ColumnExpressionArgument[bool]] = []

        if user_id:
            where_clauses.append(self.repository.model.id == user_id)
        if email:
            where_clauses.append(self.repository.model.email == email)
        if phone:
            where_clauses.append(self.repository.model.phone == phone)

        return await self.repository._crud.select_many(
            **where_clauses, limit=limit, offset=offset
        )

    async def exists(self, user_id: int) -> bool:
        return await self.repository._crud.exists(self.repository.model.id == user_id)
