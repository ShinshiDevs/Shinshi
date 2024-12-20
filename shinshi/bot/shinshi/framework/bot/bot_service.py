from collections.abc import Sequence

from hikari.impl import CacheComponents, CacheSettings, HTTPSettings
from hikari.intents import Intents
from hikari.presences import Activity, Status

from shinshi.abc.i18n.ii18n_provider import II18nProvider
from shinshi.framework.bot.bot import Bot
from shinshi.utils.env import getenv

MAX_MESSAGES: int = 100
MAX_DM_CHANNELS_IDS: int = 0


class BotService:
    __slots__: Sequence[str] = (
        "cache_settings",
        "http_settings",
        "_bot",
        "_client",
        "activity",
        "status",
        "intents",
        "shard_ids",
        "shard_count",
    )

    def __init__(
        self,
        i18n_provider: II18nProvider,
        *,
        banner: str | None = None,
        cache_settings: CacheSettings | None = None,
        cache_components: CacheComponents = CacheComponents.NONE,
        http_settings: HTTPSettings | None = None,
        intents: Intents = Intents.NONE,
        auto_chunk_members: bool = True,
        rest_url: str | None = None,
        activity: Activity | None = None,
        status: Status = Status.ONLINE,
        shard_ids: Sequence[int] | None = None,
        shard_count: int | None = None,
    ) -> None:
        self._bot: Bot = Bot(
            getenv("SHINSHI_DISCORD_TOKEN"),
            banner=banner,
            cache_settings=cache_settings
            or CacheSettings(
                components=cache_components, max_messages=MAX_MESSAGES, max_dm_channel_ids=MAX_DM_CHANNELS_IDS
            ),
            http_settings=http_settings or HTTPSettings(enable_cleanup_closed=True),
            intents=intents,
            auto_chunk_members=auto_chunk_members,
            rest_url=rest_url,
        )
        self.activity: Activity | None = activity
        self.status: Status = status
        self.shard_ids: Sequence[int] | None = shard_ids
        self.shard_count: int | None = shard_count

    @property
    def bot(self) -> Bot:
        return self._bot

    async def start(self) -> None:
        await self._bot.start(
            check_for_updates=False,
            activity=self.activity,
            status=self.status,
            shard_ids=self.shard_ids,
            shard_count=self.shard_count,
        )

    async def stop(self) -> None:
        await self._bot.close()
