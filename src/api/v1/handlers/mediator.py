from typing import Any, Callable, Type, TypeVar, cast

from src.common.interfaces.handler import Handler

HandlerType = TypeVar("HandlerType", bound=Handler)
CT = TypeVar("CT")
RT = TypeVar("RT")


def _resolve_factory(
    handler_factory: Callable[..., HandlerType],
) -> HandlerType:
    return handler_factory()


class MediatorImpl:
    def __init__(self) -> None:
        """Initialize the Mediator object by setting up dependencies dictionary."""
        self._dependencies: dict[Any, Any] = {}

    def register(
        self,
        query: Type[CT],
        handler_factory: Callable[..., HandlerType],
    ) -> None:
        """Register a handler factory for a specific query type.

        Args:
        ----
            query (Type[CT]): The type of query to register the handler for.
            handler_factory (Callable[..., HandlerType]): The factory function that creates a handler for the query type.

        """
        self._dependencies[query] = handler_factory

    async def send(self, query: CT, **kwargs: Any) -> RT:
        handler = _resolve_factory(self._dependencies[type(query)])
        return cast(RT, await handler(query, **kwargs))
