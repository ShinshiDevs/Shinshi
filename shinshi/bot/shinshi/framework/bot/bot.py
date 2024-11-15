import time
from collections.abc import Sequence
from typing import Any

from hikari.impl import GatewayBot

from shinshi.framework.bot.cache import Cache


class Bot(GatewayBot):
    __slots__: Sequence[str] = ("__cache", "uptime")

    def __init__(self, *args, **kwargs) -> None:
        self.__cache: Cache = Cache(self, settings=kwargs.pop("cache_settings"))
        self.uptime: float | None = None
        super().__init__(*args, **kwargs)

    @property
    def cache(self) -> Cache:
        return self.__cache

    @property  # type: ignore
    def _cache(self) -> Cache:  # type: ignore
        return self.__cache

    @_cache.setter
    def _cache(self, ot: Any) -> None:
        pass

    async def start(self, *args, **kwargs) -> None:
        self.uptime = time.time()
        return await super().start(*args, **kwargs)

    async def close(self) -> None:
        self.uptime = None
        return await super().close()
