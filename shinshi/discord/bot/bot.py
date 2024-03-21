from typing import Dict, Any

import hikari

from shinshi.data import DataProvider
from shinshi.discord.bot.bot_base import BotBase


class Bot(BotBase):
    def __init__(
        self,
        data_provider: DataProvider,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.__data_provider: DataProvider = data_provider

    def get_guild_count(self) -> int:
        return len(self.cache.get_guilds_view())

    def get_member_count(self) -> int:
        return sum(
            self.cache.get_guild(guild).member_count for guild in self.cache.get_guilds_view()
        )

    def get_emoji(self, *keys: str) -> hikari.KnownCustomEmoji | str:
        emoji: Dict[str, Any] | int = self.__data_provider.get_file("emojis")
        for key in keys:
            if isinstance(emoji, dict) and key in emoji:
                emoji = emoji.get(key)
            else:
                return key
        return self.cache.get_emoji(emoji)
