import abc
from typing import Any, Protocol


class Handler(Protocol):
    def __init__(self, **dependencies: Any) -> None: ...

    @abc.abstractmethod
    async def __call__(self, query: Any, **kwargs: Any) -> Any:
        """Process the query asynchronously and return the result.

        Args:
        ----
            query (Any): The query object to be processed.

        Returns:
        -------
            Any: The result of processing the query.

        """
        raise NotImplementedError

    @abc.abstractmethod
    async def handle(self, query: Any, **kwargs: Any) -> Any:
        """Handle the query asynchronously and return the result.

        Args:
        ----
            query (Any): The query object to be handled.

        Returns:
        -------
            Any: The result of handling the query.

        """
        raise NotImplementedError
