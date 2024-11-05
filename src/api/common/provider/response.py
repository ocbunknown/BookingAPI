from types import TracebackType
from typing import (
    Any,
    Mapping,
    Optional,
    Protocol,
    Type,
)


class JsonResponse(Protocol):
    async def json(self, **kwargs: Any) -> Any: ...


class TextResponse(Protocol):
    async def text(self, **kwargs: Any) -> str: ...


class BytesResponse(Protocol):
    async def read(self) -> bytes: ...


class UrlResponse(Protocol):
    @property
    def url(self) -> str: ...


class StatusResponse(Protocol):
    @property
    def status(self) -> int: ...


class HeadersResponse(Protocol):
    @property
    def headers(self) -> Mapping[str, Any]: ...


class CookiesResponse(Protocol):
    @property
    def cookies(self) -> Mapping[str, Any]: ...


class ContextManagerResponse(Protocol):
    async def __aenter__(self) -> "ContextManagerResponse": ...

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None: ...


class Response(
    JsonResponse,
    TextResponse,
    BytesResponse,
    HeadersResponse,
    CookiesResponse,
    UrlResponse,
    StatusResponse,
    ContextManagerResponse,
):
    pass
