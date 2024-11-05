from typing import Type

from src.common.dtos.base import DTOType
from src.database.models.base import ModelType


def from_model_to_dto(model: ModelType, dto: Type[DTOType]) -> DTOType:
    return dto(**model.as_dict())
