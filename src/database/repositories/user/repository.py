from typing import Type

from src.database.models import User
from src.database.repositories.base import BaseRepository
from src.database.repositories.user.reader import UserReader
from src.database.repositories.user.writer import UserWriter


class UserRepository(BaseRepository[User]):
    __slots__ = ()
    model: Type[User] = User

    def reader(self) -> UserReader:
        return UserReader(self)

    def writer(self) -> UserWriter:
        return UserWriter(self)
