import concurrent.futures
import logging
from typing import Dict, Any

import hikari
import orjson
from hikari.emojis import KnownCustomEmoji
from hikari.impl import GatewayBot, config
from hikari.intents import Intents
from hikari.presences import Activity, ActivityType
from hikari.users import OwnUser

from shinshi import LOGGER
from shinshi.bot.cache import Cache
from shinshi.data import DataProvider
from shinshi.events import event_manager, StartingEvent, StoppingEvent


class Bot(GatewayBot):
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
        self.__logger: logging.Logger = LOGGER.getChild("gateway")
        self._cache: Cache = Cache(self)
        self.print_banner(banner, allow_color, force_color, banner_extras)
        super().__init__(
            token=token,
            banner=None,
            executor=executor,
            http_settings=http_settings,
            cache_settings=self._cache.settings,
            dumps=orjson.dumps,
            loads=orjson.loads,
            intents=intents,
        )
        self.__emojis: Dict[str, Any] = data_provider.get_file("emojis")

        event_manager.subscribe(StartingEvent, self.start)
        event_manager.subscribe(StoppingEvent, self.stop)
        self.event_manager.subscribe(hikari.StartedEvent, self._set_shards_activities)

    async def _set_shards_activities(self, _) -> None:
        for _, shard in self.shards.items():
            await shard.update_presence(
                activity=Activity(
                    type=ActivityType.WATCHING,
                    name=f"Shard #{shard.id + 1} / {self.shard_count}"
                )
            )

    @property
    def me(self) -> OwnUser:
        user: OwnUser = self.get_me()
        assert user
        return user

    def get_emoji(self, *keys: str) -> KnownCustomEmoji | str:
        emoji: Dict[str, Any] | int = self.__emojis
        for key in keys:
            if isinstance(emoji, dict) and key in emoji:
                emoji = emoji.get(key)
            else:
                return key
        return self.cache.get_emoji(emoji)

    async def start(self, *args, **kwargs) -> None:
        await super().start(*args, **kwargs)

    async def stop(self) -> None:
        await self.close()
