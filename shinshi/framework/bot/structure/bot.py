from typing import Any

from hikari.impl import GatewayBot
from hikari.users import OwnUser

from .cache import Cache


class Bot(GatewayBot):
    def __init__(self, **kwargs) -> None:
        self.__cache = Cache(self)
        super().__init__(**kwargs)

    @property
    def cache(self) -> Cache:
        return self.__cache

    @property
    def _cache(self) -> Cache:
        return self.__cache

    @_cache.setter
    def _cache(self, ot: Any) -> None:
        pass

    @property
    def me(self) -> OwnUser:
        user: OwnUser = self.get_me()
        assert user
        return user
