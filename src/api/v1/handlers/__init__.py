import inspect
from typing import Any, Callable, Optional, Union

from src.common import dtos
from src.common.interfaces.handler import Handler

from . import commands, queries
from .mediator import MediatorImpl


def setup_mediator(mediator: MediatorImpl, **kw: Any) -> None:
    mediator.register(dtos.SelectUser, queries.GetUserHandler)
    mediator.register(dtos.CreateUser, commands.CreateUserHandler)
    mediator.register(dtos.DeleteUser, commands.DeleteUserHandler)
    mediator.register(dtos.UpdateUserQuery, commands.UpdateUserHandler)

    register_dependencies(mediator, **kw)


def _predict_dependency_or_raise(
    actual: dict[str, Any],
    expectable: dict[str, Any],
    non_checkable: Optional[set[str]] = None,
) -> dict[str, Any]:
    if not non_checkable:
        non_checkable = set()

    missing = [k for k in actual if k not in expectable and k not in non_checkable]
    if missing:
        details = ", ".join(f"`{k}`:`{actual[k]}`" for k in missing)
        raise TypeError(f"Did you forget to set dependency for {details}?")

    return {k: expectable.get(k, actual[k]) for k in actual}


def create_command_lazy(
    command_cls: type[Handler], **dependencies: Union[Callable[[], Any], Any]
) -> Callable[[], Handler]:
    def _create() -> Handler:
        return command_cls(
            **{k: v() if callable(v) else v for k, v in dependencies.items()}
        )

    return _create


def _retrieve_command_params(command_cls: type[Handler]) -> dict[str, Any]:
    return {
        k: v.annotation
        for k, v in inspect.signature(command_cls.__init__).parameters.items()
        if k != "self"
    }


def register_dependencies(mediator: MediatorImpl, **kw: Any) -> None:
    handlers = {}

    for query, handler_cls in mediator._dependencies.items():
        handlers[query] = {
            "handler_cls": handler_cls,
            **_retrieve_command_params(handler_cls),
        }

    for query, handler_info in handlers.items():
        handler_cls = handler_info.pop("handler_cls")
        dependencies = _predict_dependency_or_raise(handler_info, kw)
        mediator.register(
            query=query,
            handler_factory=create_command_lazy(handler_cls, **dependencies),
        )


__all__ = ("MediatorImpl",)
