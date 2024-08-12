import subprocess
from collections.abc import Sequence
from functools import cache

from aurum.commands import SlashCommand
from aurum.l10n import Localized
from hikari.embeds import Embed
from hikari.guilds import GatewayGuild

from shinshi import __version__
from shinshi.colour import Colour
from shinshi.context import Context
from shinshi.utils.icon import get_icon


class AboutCommand(SlashCommand):
    def __init__(self) -> None:
        super().__init__(
            "about", description=Localized(value="commands.about.description")
        )

    @staticmethod
    @cache
    def get_git_sha() -> str:
        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
            .decode("ascii")
            .strip()
        )

    async def callback(self, context: Context) -> None:
        guilds: Sequence[GatewayGuild] = context.bot.cache.get_guilds_view().values()
        embed: Embed = (
            Embed(
                colour=Colour.GREY,
                description=context.locale.get("commands.about.bot.description"),
            )
            .set_author(name=context.bot.me.username, icon=get_icon("info"))
            .set_thumbnail(context.bot.me.avatar_url)
            .add_field(
                name=context.locale.get("commands.about.fields.guilds"),
                value=len(guilds),
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.about.fields.members"),
                value=sum(guild.member_count for guild in guilds),
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.about.fields.latency"),
                value=f"{context.bot.heartbeat_latency * 1000:.1f} ms",
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.about.fields.version"),
                value=f"{__version__!s} ([`{self.get_git_sha()}`](https://github.com/ShinshiDevs/Shinshi/commit/{self.get_git_sha()}))",
                inline=True,
            )
        )
        return await context.create_response(embed=embed)
