from collections.abc import Sequence

from aurum.commands import SlashCommand
from aurum.l10n import Localized
from hikari.embeds import Embed
from hikari.guilds import GatewayGuild

from shinshi import __version__
from shinshi.enums.colour import Colour
from shinshi.types.context import Context
from shinshi.utils.memory_usage import get_memory_usage
from shinshi.utils.size import humanize_size


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
                value=f"[{__version__}](https://github.com/ShinshiDevs/Shinshi/releases/tag/{__version__})",
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.stats.fields.memory_usage"),
                value=humanize_size(get_memory_usage()),
                inline=True,
            )
        )
        return await context.create_response(embed=embed)
