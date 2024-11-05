from typing import TypeVar

from pydantic import BaseModel

DTOType = TypeVar("DTOType", bound="DTO")


class DTO(BaseModel):
    pass
