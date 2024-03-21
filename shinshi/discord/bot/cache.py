from typing import Tuple

from cachetools import LFUCache
from hikari.guilds import Member
from hikari.impl import CacheComponents, CacheSettings, CacheImpl
from hikari.impl import GatewayBot

DM_CHANNEL_CACHE_SIZE: int = 0
MEMBER_CACHE_SIZE: int = 1_000
MESSAGE_CACHE_SIZE: int = 1_00
MESSAGE_NULL_CACHE_SIZE: int = 1_000
CHANNEL_NULL_CACHE_SIZE: int = 1_000


class Cache(CacheImpl):
    components: CacheComponents = (
        CacheComponents.ME
        | CacheComponents.GUILDS
        | CacheComponents.GUILD_CHANNELS
        | CacheComponents.MEMBERS
        | CacheComponents.EMOJIS
        | CacheComponents.ROLES
    )

    def __init__(
        self,
        bot: GatewayBot,
    ) -> None:
        settings: CacheSettings = CacheSettings(
            components=self.components,
            max_messages=MESSAGE_CACHE_SIZE,
            max_dm_channel_ids=DM_CHANNEL_CACHE_SIZE,
        )
        super().__init__(bot, settings=settings)
        self.__null_messages: LFUCache[int, None] = LFUCache(MESSAGE_NULL_CACHE_SIZE)
        self.__null_channels: LFUCache[int, None] = LFUCache(CHANNEL_NULL_CACHE_SIZE)
        self.__members: LFUCache[Tuple[int, ...], Member | None] = LFUCache(
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
