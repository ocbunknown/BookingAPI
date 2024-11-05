from types import MappingProxyType
from typing import Dict, List, Mapping, Type

from sqlalchemy.orm import RelationshipProperty

from src.database.models.base import Base

from .user import User

__all__ = (
    "Base",
    "User",
)


def _retrieve_relationships() -> (
    Dict[Type[Base], List[RelationshipProperty[Type[Base]]]]
):
    return {
        mapper.class_: list(mapper.relationships.values())
        for mapper in Base.registry.mappers
    }


MODELS_RELATIONSHIPS_NODE: Mapping[
    Type[Base], List[RelationshipProperty[Type[Base]]]
] = MappingProxyType(_retrieve_relationships())
