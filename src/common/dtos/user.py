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


class UpdateUser(DTO):
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class DeleteUser(DTO):
    id: int
    email: Optional[str] = None
    phone: str


class UpdatePartial(DTO):
    id: int
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
