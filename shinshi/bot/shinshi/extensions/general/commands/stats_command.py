import platform
from datetime import UTC, datetime, timedelta
from typing import Any, ValuesView

from aurum.commands import SlashCommand
from aurum.l10n import Localized
from hikari import Embed, GatewayGuild
from humanize import naturalsize
from tortoise import Tortoise
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.exceptions import ConfigurationError

from shinshi.abc.models.context import Context
from shinshi.enums.colour import Colour
from shinshi.extensions.general.utils.get_cpu_usage import get_cpu_usage
from shinshi.extensions.general.utils.get_memory_usage import get_memory_usage
from shinshi.utils.icons import get_icon
from shinshi.utils.timestamp import format_datetime, format_timestamp


class StatsCommand(SlashCommand):
    def __init__(self) -> None:
        super().__init__(
            "stats",
            description=Localized(value="commands.stats.description"),
        )

    @staticmethod
    async def get_database_uptime(connection: BaseDBAsyncClient) -> timedelta:
        data: tuple[dict[str, Any]] = await connection.execute_query_dict(
            "SELECT pg_postmaster_start_time() AS start_time"
        )
        return datetime.now(UTC) - data[0]["start_time"]

    @staticmethod
    async def get_database_stats(connection: BaseDBAsyncClient) -> dict[str, Any]:
        data: tuple[dict[str, Any]] = await connection.execute_query_dict(
            "SELECT xact_commit, xact_rollback, blks_read, blks_hit, "
            "tup_returned, tup_inserted, tup_updated, tup_deleted "
            "FROM pg_stat_database WHERE datname = current_database();"
        )
        return data[0]

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
                    f"[{context.bot.version.version}]"
                    f"(https://github.com/ShinshiDevs/Shinshi/releases/tag/{context.bot.version.version}) "
                    f"([`{context.bot.version.git_sha}`]"
                    f"(https://github.com/ShinshiDevs/Shinshi/commit/{context.bot.version.git_sha}))"
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
                value=f"{get_cpu_usage():.2f}%",
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.stats.fields.memory_usage"),
                value=naturalsize(get_memory_usage()),
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

        try:
            connection: BaseDBAsyncClient = Tortoise.get_connection("default")
            database_uptime: datetime = await self.get_database_uptime(connection)
            database_stats: dict[str, Any] = await self.get_database_stats(connection)

            uptime_seconds = database_uptime.total_seconds()
            reads_per_second = database_stats["tup_returned"] / uptime_seconds
            writes_per_second = (
                database_stats["tup_inserted"]
                + database_stats["tup_updated"]
                + database_stats["tup_deleted"]
            ) / uptime_seconds

            embed.add_field(
                name=context.locale.get("commands.stats.fields.database_uptime"),
                value=format_datetime(database_uptime, "R"),
                inline=True,
            )
            embed.add_field(
                name=context.locale.get("commands.stats.fields.database_queries.name"),
                value=context.locale.get(
                    "commands.stats.fields.database_queries.value",
                    {
                        "reads": round(reads_per_second, 2),
                        "writes": round(writes_per_second, 2),
                    },
                ),
                inline=True,
            )
        except (ConfigurationError, ConnectionError):
            pass

        return await context.create_response(embed=embed)
