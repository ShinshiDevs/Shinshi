from collections import defaultdict
from collections.abc import Mapping, MutableMapping

from hikari.applications import Application
from hikari.emojis import CustomEmoji, KnownCustomEmoji
from hikari.impl import CacheImpl, CacheSettings
from hikari.snowflakes import Snowflake, SnowflakeishOr
from hikari.traits import RESTAware


class Cache(CacheImpl):
    _application_emojis_entries: MutableMapping[Snowflake, KnownCustomEmoji]

    def __init__(self, app: RESTAware, settings: CacheSettings) -> None:
        self._app = app
        self._settings = settings
        self._create_cache()
        super().__init__(app, settings)

    def _create_cache(self) -> None:
        self._application_emojis_entries = defaultdict()
        super()._create_cache()

    async def fetch_application_emojis(self) -> Mapping[Snowflake, KnownCustomEmoji]:
        application: Application = await self._app.rest.fetch_application()
        emojis: Mapping[Snowflake, KnownCustomEmoji] = {
            emoji.id: emoji
            for emoji in await self._app.rest.fetch_application_emojis(application)
        }
        self._application_emojis_entries.update(emojis)
        return emojis

    async def get_application_emoji(
        self, emoji: SnowflakeishOr[CustomEmoji]
    ) -> KnownCustomEmoji:
        application: Application = await self._app.rest.fetch_application()
        emoji_data: KnownCustomEmoji | None = self._application_emojis_entries.get(
            emoji
        )
        if emoji_data is None:
            emoji_data = await self._app.rest.fetch_application_emoji(
                application, emoji
            )
            self._application_emojis_entries[emoji_data.id] = emoji
        return emoji_data
