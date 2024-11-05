import inspect
from typing import Any, Callable, Optional, Union

from src.common import dtos
from src.common.interfaces.handler import Handler

from . import commands, queries
from .mediator import MediatorImpl


def setup_mediator(mediator: MediatorImpl, **dependencies: Any) -> None:
    mediator.register(dtos.SelectUser, queries.GetUserHandler)
    mediator.register(dtos.CreateUser, commands.CreateUserHandler)
    mediator.register(dtos.DeleteUser, commands.DeleteUserHandler)
    mediator.register(dtos.UpdateUserQuery, commands.UpdateUserHandler)

    # Removing this line will disable Dependency Injection,
    # which here functions simply as aggregation in the handlers.
    register_dependencies(mediator, **dependencies)


def _predict_dependency_or_raise(
    provided: dict[str, Any],
    required: dict[str, Any],
    non_checkable: Optional[set[str]] = None,
) -> dict[str, Any]:
    non_checkable = non_checkable or set()
    missing = [k for k in provided if k not in required and k not in non_checkable]
    if missing:
        missing_details = ", ".join(f"`{k}`:`{provided[k]}`" for k in missing)
        raise TypeError(f"Did you forget to set dependency for {missing_details}?")

    return {k: required.get(k, provided[k]) for k in provided}


def create_command_lazy(
    command_cls: type[Handler], **dependencies: Union[Callable[[], Any], Any]
) -> Callable[[], Handler]:
    def _create() -> Handler:
        return command_cls(
            **{
                name: dep() if callable(dep) else dep
                for name, dep in dependencies.items()
            }
        )

    return _create


def _retrieve_command_params(command_cls: type[Handler]) -> dict[str, Any]:
    return {
        name: param.annotation
        for name, param in inspect.signature(command_cls.__init__).parameters.items()
        if name != "self"
    }


def register_dependencies(mediator: MediatorImpl, **dependencies: Any) -> None:
    handlers = {
        query: {"handler_cls": handler_cls, **_retrieve_command_params(handler_cls)}
        for query, handler_cls in mediator._dependencies.items()
    }

    for query, handler_info in handlers.items():
        handler_cls = handler_info.pop("handler_cls")
        handler_dependencies = _predict_dependency_or_raise(handler_info, dependencies)
        mediator.register(
            query=query,
            handler_factory=create_command_lazy(handler_cls, **handler_dependencies),
        )


__all__ = ("MediatorImpl",)
