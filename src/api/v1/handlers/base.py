import abc
from typing import Any, Generic, TypeVar

from src.common.interfaces.handler import Handler

QueryType = TypeVar("QueryType")
ResultType = TypeVar("ResultType")


class BaseHandler(Handler, Generic[QueryType, ResultType]):
    async def __call__(self, query: QueryType, **kwargs: Any) -> ResultType:
        return await self.handle(query, **kwargs)

    @abc.abstractmethod
    async def handle(self, query: QueryType, **kwargs: Any) -> ResultType:
        raise NotImplementedError
