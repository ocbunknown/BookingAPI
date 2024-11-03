from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.api.common.responses import OkResponse
from src.api.v1.handlers.commands import (
    CreateUser,
    DeleteUser,
    UpdateUser,
)
from src.api.v1.handlers.queries import GetUser
from src.common import dtos
from src.common.interfaces.mediator import MediatorProtocol

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=dtos.User,
)
async def create_user_endpoint(
    mediator: Annotated[MediatorProtocol, Depends()],
    body: CreateUser,
) -> OkResponse[dtos.User]:
    return OkResponse(
        await mediator.send(body),
    )


@user_router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=dtos.User,
)
async def get_user_by_id_endpoint(
    mediator: Annotated[MediatorProtocol, Depends()],
    user_id: int,
) -> OkResponse[dtos.User]:
    return OkResponse(
        await mediator.send(GetUser(user_id=user_id)),
    )


@user_router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=dtos.DeleteUser,
)
async def delete_user_endpoint(
    mediator: Annotated[MediatorProtocol, Depends()],
    user_id: int,
) -> OkResponse[dtos.DeleteUser]:
    return OkResponse(
        await mediator.send(DeleteUser(user_id=user_id)),
    )


@user_router.patch(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=dtos.User,
)
async def update_user_endpoint(
    mediator: Annotated[MediatorProtocol, Depends()],
    user_id: int,
    body: dtos.UpdateUser,
) -> OkResponse[dtos.User]:
    return OkResponse(await mediator.send(UpdateUser(id=user_id, **body.model_dump())))
