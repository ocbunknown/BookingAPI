from typing import (
    Any,
    Final,
    List,
    Literal,
    Optional,
    TypeVar,
    Union,
)

import orjson
import redis.asyncio as aioredis

from src.common.dtos.base import DTO
from src.common.serializers.orjson import orjson_dumps
from src.core.settings import RedisSettings

ValueType = TypeVar("ValueType", float, int, str, bytes, bool)


class NonSerializableObjectsProvidedError(Exception):
    pass


ONE_MINUTE: Final[int] = 60
ONE_HOUR: Final[int] = 3600
ONE_DAY: Final[int] = 86_400
ONE_MONTH: Final[int] = 2_592_000


def _str_key(key: Any) -> str:
    return str(key)


class RedisCache:
    __slots__ = ("_redis",)

    # why mypy thinks that Redis is Generic if it isn't.
    def __init__(self, redis: aioredis.Redis) -> None:  # type: ignore
        self._redis = redis

    async def get_single(self, key: Any) -> Optional[str]:
        return await self._redis.get(_str_key(key))

    async def set_single(
        self,
        key: Union[str, Any],
        value: ValueType,
        expire_seconds: Optional[int] = ONE_HOUR,
        expire_milliseconds: Optional[int] = None,
        return_origin: bool = True,
        **additional: Any,
    ) -> Optional[Union[ValueType, bool]]:
        serialized = None
        if isinstance(value, (DTO, dict, list)):
            try:
                serialized = orjson_dumps(value)
            except orjson.JSONDecodeError as e:
                raise NonSerializableObjectsProvidedError(
                    "Some of the objects that you've provided are not serializable"
                ) from e

        set_value = await self._redis.set(
            _str_key(key),
            serialized or value,
            ex=expire_seconds,
            px=expire_milliseconds,
            **additional,
        )
        if return_origin:
            return value

        return set_value

    async def delete(self, *keys: Any) -> None:
        r_keys = (_str_key(key) for key in keys)
        await self._redis.delete(*r_keys)

    async def set_list(
        self,
        key: Any,
        *values: str,
        side: Literal["right", "left"] = "left",
        expire_seconds: Optional[int] = None,
        expire_milliseconds: Optional[int] = None,
    ) -> int:
        key = _str_key(key)

        push = self._redis.lpush if side == "left" else self._redis.rpush

        result = await push(key, *values)

        if expire_seconds:
            await self._redis.expire(key, expire_seconds)
        if expire_milliseconds:
            await self._redis.pexpire(key, expire_milliseconds)

        return result

    async def get_list(self, key: Any, start: int = 0, end: int = -1) -> List[str]:
        return await self._redis.lrange(_str_key(key), start, end)

    async def pop(self, key: Any, value: str, count: int = 0) -> int:
        return await self._redis.lrem(_str_key(key), count, value)


def get_redis(settings: RedisSettings, **kw: Any) -> RedisCache:
    return RedisCache(
        aioredis.Redis(
            host=settings.host,
            port=settings.port,
            password=settings.password,
            decode_responses=True,
            **kw,
        )
    )
