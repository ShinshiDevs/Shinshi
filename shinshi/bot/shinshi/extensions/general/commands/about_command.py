from collections.abc import ValuesView
from random import choice

from aurum.commands import SlashCommand
from hikari.embeds import Embed
from hikari.guilds import GatewayGuild

from shinshi.enums.colour import Colour
from shinshi.extensions.general.utils.round_to_significant_digit import round_to_significant_digit
from shinshi.framework.context.context import Context
from shinshi.framework.i18n.localized import Localized


class AboutCommand(SlashCommand):
    def __init__(self) -> None:
        super().__init__(name="about", description=Localized("commands.about.description"), is_dm_enabled=True)

    async def callback(self, context: Context) -> None:
        guilds: ValuesView[GatewayGuild] = context.bot.cache.get_guilds_view().values()
        members_count: int = sum(guild.member_count or 0 for guild in guilds)
        embed: Embed = (
            Embed(colour=Colour.GREY, description=context.locale.get("commands.about.bot.description"))
            .set_author(name=context.bot.me.username)
            .set_thumbnail(context.bot.me.avatar_url)
            .set_footer(
                text=choice(context.locale.get_list("commands.about.bot.interesting_facts")).format(
                    servers=f"{round_to_significant_digit(len(guilds)):,}",
                    members=f"{round_to_significant_digit(members_count):,}",
                )
            )
        )
        return await context.create_response(embed=embed)
