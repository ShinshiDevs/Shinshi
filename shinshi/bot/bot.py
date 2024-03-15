import concurrent.futures
import datetime
import logging
from typing import Dict, Any

import orjson
from hikari.emojis import KnownCustomEmoji
from hikari.impl import GatewayBot, GatewayShardImpl, config
from hikari.intents import Intents
from hikari.presences import Activity, ActivityType, Status
from hikari.users import OwnUser

from shinshi.bot.cache import Cache
from shinshi.data import DataProvider


class Bot(GatewayBot):
    def __init__(
        self,
        token: str,
        *,
        allow_color: bool = True,
        banner: str | None = "shinshi",
        banner_extras: Dict[str, Any],
        executor: concurrent.futures.Executor | None = None,
        force_color: bool = False,
        http_settings: config.HTTPSettings | None = None,
        intents: Intents = Intents.ALL_UNPRIVILEGED,
        data_provider: DataProvider,
    ) -> None:
        self.__logger: logging.Logger = logging.getLogger("shinshi.gateway")
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
        logger: logging.Logger = self.__logger.getChild(str(shard_id))
        if activity is None:
            activity: Activity | None = Activity(
                type=ActivityType.WATCHING,
                name=f"Shard #{shard_id + 1} / {shard_count}"
            )
        new_shard: GatewayShardImpl = GatewayShardImpl(
            http_settings=self._http_settings,
            proxy_settings=self._proxy_settings,
            event_manager=self._event_manager,
            event_factory=self._event_factory,
            intents=self._intents,
            dumps=self._dumps,
            loads=self._loads,
            initial_activity=activity,
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
            await new_shard.start()
            if new_shard.is_alive:
                logger.debug("shard %s started successfully", shard_id)
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
        emoji: Dict[str, Any] | int = self.__emojis
        for key in keys:
            if isinstance(emoji, dict) and key in emoji:
                emoji = emoji.get(key)
            else:
                return key
        return self.cache.get_emoji(emoji)
