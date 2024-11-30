from collections.abc import Iterable

from aurum.commands.decorators import sub_command
from aurum.commands.options import Option
from aurum.commands.slash_command import SlashCommandGroup
from hikari.commands import OptionType
from hikari.embeds import Embed
from hikari.guilds import Role
from hikari.interactions import InteractionMember
from hikari.users import User

from shinshi.enums.colour import Colour
from shinshi.framework.context.context import Context
from shinshi.framework.i18n.localized import Localized
from shinshi.utils.timestamp import format_datetime

MAX_ROLES: int = 5


class UserCommand(SlashCommandGroup):
    def __init__(self) -> None:
        super().__init__(name="user")

    @sub_command(
        name="info",
        description=Localized("commands.user.info.description"),
        options=[
            Option(
                type=OptionType.USER,
                name="user",
                description=Localized("commands.user.options.user.description"),
                is_required=False,
            )
        ],
    )
    async def user_info(self, context: Context, user: User | InteractionMember | None = None) -> None:
        if not user:
            user = context.member or context.interaction.user
        embed: Embed = (
            Embed(colour=user.accent_colour or Colour.GREY, title=str(user.display_name))
            .add_field(
                name=context.locale.get("commands.user.info.fields.created_at"),
                value=format_datetime(user.created_at),
                inline=True,
            )
            .set_footer(text=f"ID: {user.id}")
            .set_thumbnail(user.display_avatar_url)
        )
        if user.display_name and user.display_name.lower() != user.username.lower():
            embed.set_author(name=user.username)
        if isinstance(user, InteractionMember):
            member: InteractionMember = user
            if member.joined_at:
                embed.add_field(
                    name=context.locale.get("commands.user.info.fields.joined_at", {"guild": context.guild.name}),
                    value=format_datetime(member.joined_at),
                    inline=True,
                )

            roles: Iterable[Role] = sorted(
                filter(lambda role: role.id != context.interaction.guild_id, user.get_roles()),
                key=lambda role: role.position, reverse=True
            )
            if roles:
                embed.colour = next(filter(lambda role: role.colour, roles), embed).colour
                embed.add_field(
                    name=context.locale.get("commands.user.info.fields.roles.name"),
                    value=str(", ".join(map(lambda role: role.mention, roles[:MAX_ROLES])) + ("..." if len(roles) > MAX_ROLES else "")),
                )
            else:
                embed.add_field(
                    name=context.locale.get("commands.user.info.fields.roles.name"),
                    value=context.locale.get("commands.user.info.fields.roles.default"),
                )
        await context.create_response(embed=embed)
