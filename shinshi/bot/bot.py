from typing import Dict, Any

from hikari import OwnUser, KnownCustomEmoji
from hikari.impl.gateway_bot import GatewayBot

from shinshi.bot.cache import Cache
from shinshi.providers.data.data_provider import DataProvider


class DiscordBot(GatewayBot):
    def __init__(self, data_provider: DataProvider, **kwargs) -> None:
        self._cache: Cache = Cache(self)
        self.data_provider: DataProvider = data_provider
        super().__init__(**kwargs, cache_settings=self._cache.settings)

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
