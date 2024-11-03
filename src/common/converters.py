from src.common import dtos
from src.database import models


def convert_user_model_to_dto(model: models.User) -> dtos.User:
    return dtos.User(**model.__dict__)


def convert_user_model_to_delete_user_dto(model: models.User) -> dtos.DeleteUser:
    return dtos.DeleteUser(**model.__dict__)
