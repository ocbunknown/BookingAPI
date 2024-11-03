from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from src.database import models
from src.database.repositories.base import BaseInteractor

if TYPE_CHECKING:
    from src.common import dtos


class UserWriter(BaseInteractor[models.User]):
    __slots__ = ()

    async def create(self, query: dtos.CreateUser) -> Optional[models.User]:
        return await self.repository._crud.insert(**query.model_dump())

    async def update(
        self,
        query: dtos.UpdatePartial,
    ) -> Optional[models.User]:
        result = await self.repository._crud.update(
            self.repository.model.id == query.id,
            **query.model_dump(exclude_none=True),
        )
        return result[0] if result else None

    async def delete(
        self,
        user_id: Optional[int] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> Optional[models.User]:
        if user_id:
            result = await self.repository._crud.delete(
                self.repository.model.id == user_id
            )
        elif email:
            result = await self.repository._crud.delete(
                self.repository.model.email == email
            )
        else:
            result = await self.repository._crud.delete(
                self.repository.model.phone == phone
            )

        return result[0] if result else None
