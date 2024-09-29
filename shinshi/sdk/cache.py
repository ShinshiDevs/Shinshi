from cachetools import LFUCache
from hikari.applications import Application
from hikari.impl import CacheImpl, CacheSettings
from hikari.traits import GatewayBotAware

APPLICATION_CACHE_SIZE: int = 1


class Cache(CacheImpl):
    def __init__(self, app: GatewayBotAware, settings: CacheSettings) -> None:
        super().__init__(app, settings=settings)
        self.__application_cache: LFUCache[GatewayBotAware, Application] = LFUCache(
            APPLICATION_CACHE_SIZE
        )

    def clear_safe(self) -> None:
        self.__application_cache.clear()
        self.clear_messages()
        self.clear_dm_channel_ids()

    def clear(self) -> None:
        self.clear_safe()
        super().clear()

    async def get_application(self) -> Application:
        if not self.__application_cache:
            application: Application = await self._app.rest.fetch_application()
            self.__application_cache[self._app] = application

        return self.__application_cache[self._app]
