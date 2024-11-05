from typing import Optional

from src.common.dtos.base import DTO


class User(DTO):
    id: int
    email: Optional[str] = None
    phone: str


class CreateUser(DTO):
    email: Optional[str] = None
    phone: str
    password: str


class UpdateUserQuery(DTO):
    user_id: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class UpdateUser(DTO):
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class DeleteUser(DTO):
    user_id: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class SelectUser(DeleteUser):
    pass
