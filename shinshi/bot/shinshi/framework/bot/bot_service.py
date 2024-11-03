from aurum.client import Client
from aurum.commands.enum import SyncCommandsFlag
from hikari import GatewayBotAware
from hikari.impl import CacheComponents, CacheSettings, GatewayBot, HTTPSettings
from hikari.intents import Intents
from hikari.presences import Activity, Status

from shinshi.abc.bot.ibot_service import IBotService
from shinshi.utils.env import getenv

MAX_MESSAGES: int = 100
MAX_DM_CHANNELS_IDS: int = 0


class BotService(IBotService):
    def __init__(
        self,
        *,
        cache_settings: CacheSettings | None = None,
        cache_components: CacheComponents = CacheComponents.NONE,
        http_settings: HTTPSettings | None = None,
        intents: Intents = Intents.NONE,
        auto_chunk_members: bool = True,
        rest_url: str | None = None,
        sync_commands: SyncCommandsFlag = SyncCommandsFlag.NONE,
        activity: Activity | None = None,
        status: Status = Status.ONLINE,
    ) -> None:
        self.cache_settings: CacheSettings = cache_settings or CacheSettings(
            components=cache_components,
            max_messages=MAX_MESSAGES,
            max_dm_channel_ids=MAX_DM_CHANNELS_IDS,
        )
        self.http_settings: HTTPSettings = http_settings or HTTPSettings(
            enable_cleanup_closed=True,
        )

        self._bot: GatewayBot = GatewayBot(
            getenv("SHINSHI_DISCORD_TOKEN"),
            cache_settings=cache_settings,
            http_settings=http_settings,
            intents=intents,
            auto_chunk_members=auto_chunk_members,
            rest_url=rest_url,
        )
        self._client: Client = Client(
            self._bot,
            sync_commands=sync_commands,
        )

        self.activity: Activity | None = activity
        self.status: Status = status

    @property
    def bot(self) -> GatewayBotAware:
        return self._bot

    @property
    def client(self) -> Client:
        return self._client

    async def start(self) -> None:
        await self._bot.start(
            check_for_updates=False,
            activity=self.activity,
            status=self.status,
        )

    async def stop(self) -> None:
        await self._bot.close()
