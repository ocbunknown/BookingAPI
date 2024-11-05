from __future__ import annotations

from types import TracebackType
from typing import Optional, Protocol, Type


class AsyncContextManager(Protocol):
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None: ...

    async def __aenter__(self) -> AsyncContextManager: ...
