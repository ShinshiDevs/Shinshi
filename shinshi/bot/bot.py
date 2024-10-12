from collections.abc import Callable, Sequence
from concurrent.futures import Executor
from os import PathLike
from typing import Any, Mapping

from hikari.impl import GatewayBot
from hikari.impl.config import CacheSettings, HTTPSettings, ProxySettings
from hikari.intents import Intents
from hikari.internal.data_binding import (
    default_json_dumps,
    default_json_loads,
)
from hikari.users import OwnUser

from shinshi.cache.cache import Cache


class Bot(GatewayBot):
    __slots__: Sequence[str] = ("__application", "__cache")

    def __init__(
        self,
        token: str,
        *,
        allow_color: bool = True,
        banner: str | None = "hikari",
        suppress_optimization_warning: bool = False,
        executor: Executor | None = None,
        force_color: bool = False,
        cache_settings: CacheSettings | None = None,
        http_settings: HTTPSettings | None = None,
        dumps: Callable[
            [Sequence[Any] | Mapping[str, Any]], bytes
        ] = default_json_dumps,
        loads: Callable[
            [str | bytes], Sequence[Any] | Mapping[str, Any]
        ] = default_json_loads,
        intents: Intents = Intents.ALL_UNPRIVILEGED,
        auto_chunk_members: bool = True,
        logs: None | str | int | dict[str, Any] | PathLike[str] = "INFO",
        max_rate_limit: float = 300,
        max_retries: int = 3,
        proxy_settings: ProxySettings | None = None,
        rest_url: str | None = None,
    ) -> None:
        self.__cache: Cache = Cache(self, settings=cache_settings)
        super().__init__(
            token,
            allow_color=allow_color,
            banner=banner,
            suppress_optimization_warning=suppress_optimization_warning,
            executor=executor,
            force_color=force_color,
            cache_settings=cache_settings,
            http_settings=http_settings,
            dumps=dumps,
            loads=loads,
            intents=intents,
            auto_chunk_members=auto_chunk_members,
            logs=logs,
            max_rate_limit=max_rate_limit,
            max_retries=max_retries,
            proxy_settings=proxy_settings,
            rest_url=rest_url,
        )

    @property
    def me(self) -> OwnUser:
        user: OwnUser = self.get_me()
        assert user
        return user

    @property
    def cache(self) -> Cache:
        return self.__cache

    @property  # type: ignore
    def _cache(self) -> Cache:  # type: ignore
        return self.__cache

    @_cache.setter
    def _cache(self, ot: Any) -> None:
        pass
