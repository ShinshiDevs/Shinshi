from typing import List

from aurum.commands.decorators.sub_command import sub_command
from aurum.commands.options import Option
from aurum.commands.slash_command import SlashCommandGroup
from hikari.commands import OptionType
from hikari.embeds import Embed
from hikari.snowflakes import Snowflake

from shinshi.enums.colour import Colour
from shinshi.framework.context.context import Context
from shinshi.framework.i18n.localized import Localized
from shinshi.utils.emojis import find_emojis
from shinshi.utils.timestamp import format_datetime

MAX_EMOJIS: int = 5


class EmojiCommand(SlashCommandGroup):
    def __init__(self) -> None:
        super().__init__(name="emoji")

    @sub_command(
        name="view",
        description=Localized("commands.emoji.view.description"),
        options=[
            Option(
                type=OptionType.STRING, name="emojis", description=Localized("commands.emoji.view.options.emojis.description")
            )
        ],
    )
    async def emoji_view(self, context: Context, emojis: str) -> None:
        embeds: List[Embed] = []
        matches: set[Snowflake] = set(find_emojis(emojis))

        if not matches:
            return await context.create_warning_response(context.locale.get("commands.emoji.view.errors.not_provided"))

        for match in matches:
            emoji = context.bot.cache.get_emoji(match)
            if not emoji:
                continue
            embed: Embed = (
                Embed(colour=Colour.GREY, title=emoji.name, url=emoji.url)
                .add_field(
                    name=context.locale.get("commands.emoji.view.fields.created_at"),
                    value=format_datetime(emoji.created_at),
                    inline=True,
                )
                .set_footer(f"ID: {emoji.id}")
                .set_thumbnail(emoji.url)
            )
            embed.add_field(
                name=context.locale.get("commands.emoji.view.fields.available"),
                value=context.locale.get("special.affirmative") if emoji.is_available else context.locale.get("special.negative"), inline=True
            )
            if emoji.guild_id and emoji.guild_id != context.interaction.guild_id:
                embed.add_field(
                    name=context.locale.get("commands.emoji.view.fields.guild"),
                    value=context.bot.cache.get_guild(emoji.guild_id).name
                )
            embeds.append(embed)

        if not embeds:
            return await context.create_warning_response(context.locale.get("commands.emoji.view.errors.not_found"))

        elif len(embeds) > MAX_EMOJIS:
            embeds = embeds[:MAX_EMOJIS]
            embeds[-1].set_footer(f"{context.locale.get("commands.emoji.view.limit")} · {embeds[-1].footer.text}")

        return await context.create_response(embeds=embeds)
