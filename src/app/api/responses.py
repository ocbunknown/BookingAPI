from typing import Any, Generic, Mapping, Optional, TypeVar

from fastapi.responses import ORJSONResponse as _ORJSONResponse
from starlette.background import BackgroundTask

from src.app.common.serializers.orjson import orjson_dumps

ResultType = TypeVar("ResultType")


class ORJSONResponse(_ORJSONResponse):
    def render(self, content: Any) -> bytes:
        if isinstance(content, bytes):
            return content
        return orjson_dumps(content)


class OkResponse(ORJSONResponse, Generic[ResultType]):
    def __init__(
        self,
        content: ResultType,
        status_code: int = 200,
        headers: Optional[Mapping[str, str]] = None,
        media_type: Optional[str] = None,
        background: Optional[BackgroundTask] = None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type, background)
