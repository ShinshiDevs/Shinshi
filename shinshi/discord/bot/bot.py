import concurrent.futures
from typing import Dict, Any

import hikari
import orjson
from hikari.impl import GatewayBot, config
from hikari.intents import Intents
from hikari.presences import Activity, ActivityType
from hikari.users import OwnUser

from shinshi.data import DataProvider
from shinshi.discord.bot.bot_meta import BotMeta
from shinshi.discord.bot.cache import Cache
from shinshi.events import StartingEvent, StoppingEvent, event_listener


class Bot(GatewayBot, metaclass=BotMeta):
    def __init__(
        self,
        token: str,
        data_provider: DataProvider,
        *,
        allow_color: bool = True,
        banner: str | None = "shinshi",
        banner_extras: Dict[str, Any],
        executor: concurrent.futures.Executor | None = None,
        force_color: bool = False,
        http_settings: config.HTTPSettings | None = None,
        intents: Intents = Intents.ALL_UNPRIVILEGED,
    ) -> None:
        self.__cache: Cache = Cache(self)
        self.__emojis: Dict[str, Any] = data_provider.get_file("emojis")
        super().__init__(
            token=token,
            banner=None,
            executor=executor,
            http_settings=http_settings,
            cache_settings=self.__cache.settings,
            dumps=orjson.dumps,
            loads=orjson.loads,
            intents=intents,
        )
        self.print_banner(banner, allow_color, force_color, banner_extras)
        self.event_manager.subscribe(hikari.StartedEvent, self._set_shards_activities)

    @event_listener(StartingEvent)
    async def start(self, *args, **kwargs) -> None:
        await super().start(*args, **kwargs)

    @event_listener(StoppingEvent)
    async def stop(self) -> None:
        await self.close()

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

    def get_guild_count(self) -> int:
        return len(self.cache.get_guilds_view())

    def get_member_count(self) -> int:
        # TODO: put this in cache, because this construction so heavy.
        return sum(self.cache.get_guild(guild).member_count for guild in self.cache.get_guilds_view())

    def get_emoji(self, *keys: str) -> hikari.KnownCustomEmoji | str:
        emoji: Dict[str, Any] | int = self.__emojis
        for key in keys:
            if isinstance(emoji, dict) and key in emoji:
                emoji = emoji.get(key)
            else:
                return key
        return self.cache.get_emoji(emoji)

    async def _set_shards_activities(self, _) -> None:
        for _, shard in self.shards.items():
            await shard.update_presence(
                activity=Activity(
                    type=ActivityType.WATCHING,
                    name=f"Shard #{shard.id + 1} / {self.shard_count}"
                )
            )
