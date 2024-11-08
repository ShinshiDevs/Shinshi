import platform
from typing import ValuesView

from aurum.commands import SlashCommand
from aurum.l10n import Localized
from hikari.embeds import Embed
from hikari.guilds import GatewayGuild
from humanize import naturalsize
from psutil import Process

from shinshi import __version__
from shinshi.abc.models.context import Context
from shinshi.enums.colour import Colour
from shinshi.utils.icons import get_icon
from shinshi.utils.timestamp import format_timestamp


class StatsCommand(SlashCommand):
    def __init__(self) -> None:
        self.process: Process = Process()
        super().__init__(
            name="stats",
            description=Localized(value="commands.stats.description"),
            is_dm_enabled=True,
        )

    async def callback(self, context: Context) -> None:
        guilds: ValuesView[GatewayGuild] = context.bot.cache.get_guilds_view().values()
        members_count: int = sum(guild.member_count for guild in guilds)
        embed: Embed = (
            Embed(colour=Colour.GREY)
            .set_author(
                name=context.locale.get("commands.stats.embed.title"),
                icon=get_icon("server.webp"),
            )
            .add_field(
                name=context.locale.get("commands.stats.fields.version"),
                value=(
                    f"[{__version__.version}]"
                    f"(https://github.com/ShinshiDevs/Shinshi/releases/tag/{__version__.version}) "
                    f"([`{__version__.git_sha}`]"
                    f"(https://github.com/ShinshiDevs/Shinshi/commit/{__version__.git_sha}))"
                ),
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.stats.fields.uptime"),
                value=format_timestamp(context.bot.uptime, "R"),
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.stats.fields.system"),
                value=platform.system(),
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.stats.fields.latency"),
                value=f"{context.bot.heartbeat_latency * 1_000:.1f}ms",
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.stats.fields.cpu_usage"),
                value=f"{self.process.cpu_percent():.2f}%",
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.stats.fields.memory_usage"),
                value=naturalsize(self.process.memory_info().rss),
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.stats.fields.guilds"),
                value=len(guilds),
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.stats.fields.members"),
                value=members_count,
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.stats.fields.channels"),
                value=len(context.bot.cache.get_guild_channels_view()),
                inline=True,
            )
        )

        if context.guild is not None:
            embed.description = context.locale.get(
                "commands.stats.embed.description",
                {
                    "shard_id": context.guild.shard_id + 1,
                    "shard_count": context.bot.shard_count,
                },
            )

        return await context.create_response(embed=embed)
