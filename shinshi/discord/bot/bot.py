import concurrent.futures
from typing import Dict, Any, Sequence

import hikari
import orjson
from hikari.applications import Application
from hikari.impl import GatewayBot, config
from hikari.intents import Intents
from hikari.presences import Activity, ActivityType
from hikari.users import OwnUser

from shinshi.data import DataProvider
from shinshi.discord.bot.bot_meta import BotMeta
from shinshi.discord.bot.cache import Cache
from shinshi.discord.workflows.workflow_group import WorkflowGroup
from shinshi.discord.workflows.workflow_manager import WorkflowManager
from shinshi.events import event_listener
from shinshi.events.lifetime_events import StartingBotEvent, StoppingEvent
from shinshi.i18n import I18nProvider


class Bot(GatewayBot, metaclass=BotMeta):
    def __init__(
        self,
        token: str,
        i18n_provider: I18nProvider,
        data_provider: DataProvider,
        workflows: Sequence[WorkflowGroup],
        *,
        allow_color: bool = True,
        banner: str | None = "shinshi",
        banner_extras: Dict[str, Any],
        executor: concurrent.futures.Executor | None = None,
        force_color: bool = False,
        http_settings: config.HTTPSettings | None = None,
        intents: Intents = Intents.ALL_UNPRIVILEGED,
    ) -> None:
        self.application: Application | None = None
        self.__cache: Cache = Cache(self)
        self.__emojis: Dict[str, Any] = data_provider.get_file("emojis")
        self.__workflow_manager: WorkflowManager = WorkflowManager(
            self,
            i18n_provider,
            workflows
        )
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
        self.event_manager.subscribe(hikari.ShardReadyEvent, self._set_shard_activity)
        self.event_manager.subscribe(hikari.StartedEvent, self._sync_commands)

    @event_listener(StartingBotEvent)
    async def start(self, *args, **kwargs) -> None:
        self.__workflow_manager.build()
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

    async def _set_shard_activity(self, event: hikari.ShardReadyEvent) -> None:
        await event.shard.update_presence(
            activity=Activity(
                type=ActivityType.WATCHING,
                name=f"Shard #{event.shard.id + 1} / {self.shard_count}"
            )
        )

    async def _sync_commands(self, _: hikari.StartedEvent) -> None:
        if self.application is None:
            self.application = await self.rest.fetch_application()
        await self.__workflow_manager.sync_commands(self.application.id)
