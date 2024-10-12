from collections.abc import Sequence
from resource import RUSAGE_SELF, getrusage

from aurum.commands import SlashCommand
from aurum.l10n import Localized
from hikari.embeds import Embed
from hikari.guilds import GatewayGuild

from shinshi.enums.colour import Colour
from shinshi.types.context import Context
from shinshi.utils.size import humanize_size
from shinshi.utils.version import get_version


class StatisticCommand(SlashCommand):
    def __init__(self) -> None:
        super().__init__(
            "stats",
            description=Localized(value="commands.stats.description"),
            is_dm_enabled=True,
        )

    async def callback(self, context: Context) -> None:
        guilds: Sequence[GatewayGuild] = context.bot.cache.get_guilds_view().values()
        embed: Embed = (
            Embed(colour=Colour.GREY)
            .add_field(
                name=context.locale.get("commands.stats.fields.guilds"),
                value=len(guilds),
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.stats.fields.members"),
                value=sum(guild.member_count for guild in guilds),
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.stats.fields.latency"),
                value=f"{context.bot.heartbeat_latency * 1000:.1f} ms",
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.stats.fields.version"),
                value=f"[{get_version()}](https://github.com/ShinshiDevs/Shinshi/releases/tag/{get_version()})",
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.stats.fields.memory_usage"),
                value=humanize_size(getrusage(RUSAGE_SELF).ru_maxrss),
                inline=True,
            )
        )
        return await context.create_response(embed=embed)
