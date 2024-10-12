from hikari.impl import CacheImpl, CacheSettings
from hikari.traits import GatewayBotAware

APPLICATION_CACHE_SIZE: int = 1


class Cache(CacheImpl):
    def __init__(self, app: GatewayBotAware, settings: CacheSettings) -> None:
        super().__init__(app, settings=settings)

    def clear_safe(self) -> None:
        self.clear_messages()
        self.clear_dm_channel_ids()

    def clear(self) -> None:
        self.clear_safe()
        super().clear()
