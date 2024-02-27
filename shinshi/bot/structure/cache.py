from cachetools import LFUCache
from hikari.guilds import Member
from hikari.impl import CacheComponents
from hikari.impl import CacheImpl
from hikari.impl import CacheSettings
from hikari.impl import GatewayBot

DM_CHANNEL_CACHE_SIZE: int = 0
MEMBER_CACHE_SIZE: int = 1_000
MESSAGE_CACHE_SIZE: int = 1_000
MESSAGE_NULL_CACHE_SIZE: int = 1_000
CHANNEL_NULL_CACHE_SIZE: int = 1_000


class Cache(CacheImpl):
    settings: CacheSettings = CacheSettings(
        components=(
            CacheComponents.ME
        ),
        max_messages=MESSAGE_CACHE_SIZE,
        max_dm_channel_ids=DM_CHANNEL_CACHE_SIZE,
    )

    def __init__(
        self,
        bot: GatewayBot,
    ) -> None:
        super().__init__(bot, settings=self.settings)
        self.__null_messages: LFUCache[int, None] = LFUCache(MESSAGE_NULL_CACHE_SIZE)
        self.__null_channels: LFUCache[int, None] = LFUCache(CHANNEL_NULL_CACHE_SIZE)
        self.__members: LFUCache[tuple[int, ...], Member | None] = LFUCache(
            MEMBER_CACHE_SIZE
        )

    def clear_safe(self) -> None:
        self.__null_messages.clear()
        self.__null_channels.clear()
        self.__members.clear()
        self.clear_messages()
        self.clear_dm_channel_ids()

    def clear(self) -> None:
        self.clear_safe()
        super().clear()
