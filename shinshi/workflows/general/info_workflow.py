from hikari.embeds import Embed

import shinshi
from shinshi.constants import icons_dir
from shinshi.discord.interactables.decorators.slash_command import slash_command
from shinshi.discord.interactables.models.translatable import Translatable
from shinshi.discord.models.interaction_context import InteractionContext
from shinshi.discord.workflows.workflow_base import WorkflowBase
from shinshi.utils.int import get_separated_number


class InfoWorkflow(WorkflowBase):
    @slash_command(
        description=Translatable("commands.info.description"),
        dm_enabled=True
    )
    async def info(self, interaction: InteractionContext) -> None:
        embed: Embed = (
            Embed(
                title=interaction.bot.me.username,
                url="https://github.com/ShinshiDevs",
                description=interaction.translate(
                    "commands.info.embed.description",
                    {"shard": interaction.get_guild().shard_id}
                ),
            )
            .set_thumbnail(interaction.bot.me.avatar_url)
            .set_author(
                name=interaction.translate("commands.info.embed.author.name"),
                icon=icons_dir / "information",
            )
            .set_footer(text=f"{shinshi.__copyright__} ({shinshi.__license__})")
            .add_field(
                name=interaction.translate("commands.info.embed.fields.information.name"),
                value=interaction.translate(
                    "commands.info.embed.fields.information.value",
                    {
                        "guilds": get_separated_number(interaction.bot.get_guild_count()),
                        "users": get_separated_number(interaction.bot.get_member_count()),
                        "latency": f"{round(interaction.bot.heartbeat_latency * 1000, 1)}ms"
                    },
                ),
            )
        )
        return await interaction.create_response(embed=embed)
