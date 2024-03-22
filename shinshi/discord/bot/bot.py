from shinshi.discord.bot.bot_base import BotBase


class Bot(BotBase):
    def get_guild_count(self) -> int:
        return len(self.cache.get_guilds_view())

    def get_member_count(self) -> int:
        return sum(
            self.cache.get_guild(guild).member_count
            for guild in self.cache.get_guilds_view()
        )
