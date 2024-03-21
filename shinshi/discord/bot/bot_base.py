from typing import Any

from hikari.applications import Application
from hikari.impl import GatewayBot
from hikari.users import OwnUser

from shinshi.discord.bot.cache import Cache


class BotBase(GatewayBot):
    def __init__(
        self,
        *args,
        **kwargs
    ) -> None:
        self.__application: Application | None = None
        self.__cache: Cache = Cache(self)
        super().__init__(*args, **kwargs, cache_settings=self.__cache.settings)

    @property
    def application(self) -> Application:
        assert self.__application
        return self.__application

    @property
    def me(self) -> OwnUser:
        user: OwnUser = self.get_me()
        assert user
        return user

    @property
    def cache(self) -> Cache:
        return self.__cache

    @property
    def _cache(self) -> Cache:
        return self.__cache

    @_cache.setter
    def _cache(self, ot: Any) -> None:
        pass

    # TODO: Uncomment when this will be necessary
    # async def __create_application(self) -> None:
    #     if self.__application is None:
    #         self.__application = await self.rest.fetch_application()
