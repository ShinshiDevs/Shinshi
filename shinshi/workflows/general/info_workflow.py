from hikari.embeds import Embed

import shinshi
from shinshi.constants import ICONS_DIR
from shinshi.discord.interactables.decorators.slash_command import slash_command
from shinshi.discord.models.interaction_context import InteractionContext
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows.workflow_base import WorkflowBase
from shinshi.framework.utils.int import get_separated_number


class InfoWorkflow(WorkflowBase):
    @slash_command(
        description=Translatable("commands.info.description"),
        dm_enabled=True
    )
    async def info(self, context: InteractionContext) -> None:
        embed: Embed = (
            Embed(
                title=context.bot.me.username,
                url="https://github.com/ShinshiDevs",
                description=context.i18n.get(
                    "commands.info.embed.description",
                    {"shard": context.interaction.get_guild().shard_id}
                ),
            )
            .set_thumbnail(context.bot.me.avatar_url)
            .set_author(
                name=context.i18n.get("commands.info.embed.author.name"),
                icon=ICONS_DIR / "information",
            )
            .set_footer(text=f"{shinshi.__copyright__} ({shinshi.__license__})")
            .add_field(
                name=context.i18n.get("commands.info.embed.fields.information.name"),
                value=context.i18n.get(
                    "commands.info.embed.fields.information.value",
                    {
                        "guilds": get_separated_number(context.bot.get_guild_count()),
                        "users": get_separated_number(context.bot.get_member_count()),
                        "latency": f"{round(context.bot.heartbeat_latency * 1000, 1)}ms"
                    },
                ),
            )
        )
        return await context.create_response(embed=embed)
