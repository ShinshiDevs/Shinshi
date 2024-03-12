import datetime
import logging
import time
from typing import Dict, Any

from hikari import OwnUser, KnownCustomEmoji, Activity, Status, ActivityType
from hikari.impl import GatewayShardImpl
from hikari.impl.gateway_bot import GatewayBot

from shinshi.discord.bot.cache import Cache
from shinshi.providers.data.data_provider import DataProvider


class DiscordBot(GatewayBot):
    def __init__(self, data_provider: DataProvider, **kwargs) -> None:
        self.__logger: logging.Logger = logging.getLogger("shinshi.discord.bot")
        self._cache: Cache = Cache(self)
        self.data_provider: DataProvider = data_provider
        super().__init__(**kwargs, cache_settings=self._cache.settings)

    async def _start_one_shard(
        self,
        activity: Activity | None,
        afk: bool,
        idle_since: datetime.datetime | None,
        status: Status,
        large_threshold: int,
        shard_id: int,
        shard_count: int,
        url: str,
    ) -> None:
        new_shard: GatewayShardImpl = GatewayShardImpl(
            http_settings=self._http_settings,
            proxy_settings=self._proxy_settings,
            event_manager=self._event_manager,
            event_factory=self._event_factory,
            intents=self._intents,
            dumps=self._dumps,
            loads=self._loads,
            initial_activity=Activity(
                type=ActivityType.WATCHING, name=f"Shard #{shard_id + 1} / {shard_count}"
            ),
            initial_is_afk=afk,
            initial_idle_since=idle_since,
            initial_status=status,
            large_threshold=large_threshold,
            shard_id=shard_id,
            shard_count=shard_count,
            token=self._token,
            url=url,
        )
        try:
            start: float = time.monotonic()
            await new_shard.start()
            end: float = time.monotonic()
            if new_shard.is_alive:
                self.__logger.debug(
                    "shard %s started successfully in %.1fms", shard_id, (end - start) * 1_000
                )
                self._shards[shard_id] = new_shard
                return
            raise RuntimeError(f"shard {shard_id} shut down immediately when starting")
        except Exception:
            if new_shard.is_alive:
                await new_shard.close()
            raise

    @property
    def me(self) -> OwnUser:
        user: OwnUser = self.get_me()
        assert user
        return user

    def get_emoji(self, *keys: str) -> KnownCustomEmoji | str:
        emoji: Dict[str, Any] | int | str = self.data_provider.get_file("emojis")
        for key in keys:
            if isinstance(emoji, dict) and key in emoji:
                emoji = emoji.get(key)
            else:
                return key
        return self.cache.get_emoji(emoji)
