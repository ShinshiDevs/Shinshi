from typing import Iterable

from aurum.commands import SlashCommand
from aurum.commands.decorators import sub_command
from aurum.l10n import Localized
from aurum.option import Option
from hikari.commands import OptionType
from hikari.embeds import Embed
from hikari.guilds import Role
from hikari.interactions import InteractionMember
from hikari.users import PartialUser

from shinshi.ext.colour import Colour
from shinshi.sdk.context import Context
from shinshi.utils.datetime import format_datetime

COMMAND_OPTIONS: tuple[Option] = (
    Option(
        type=OptionType.USER,
        name="user",
        description=Localized(value="commands.user.options.user"),
        is_required=False,
    ),
)


class UserCommand(SlashCommand):
    def __init__(self) -> None:
        super().__init__("user", is_dm_enabled=True)

    @sub_command(
        "info",
        description=Localized(value="commands.user.info.description"),
        options=COMMAND_OPTIONS,
    )
    async def user_info(
        self,
        context: Context,
        user: InteractionMember | PartialUser | None = None,
    ) -> None:
        if user is None:
            user = context.member or context.user
        assert isinstance(user, (InteractionMember, PartialUser))
        embed: Embed = (
            Embed(
                title=user.display_name,
                description=f"-# ID: {user.id}",
                colour=user.accent_colour or Colour.GREY,
            )
            .set_thumbnail(user.display_avatar_url)
            .add_field(
                name=context.locale.get("commands.user.info.fields.created_at"),
                value=format_datetime(user.created_at, "D"),
                inline=True,
            )
        )
        if embed.title != user.username:
            embed.set_author(name=user.username)
        if isinstance(user, InteractionMember):
            roles: Iterable[Role] | list[str] = sorted(
                user.get_roles(), key=lambda role: role.position, reverse=True
            )
            embed.add_field(
                name=context.locale.get(
                    "commands.user.info.fields.joined_at", {"guild": context.guild.name}
                ),
                value=format_datetime(user.joined_at, "D"),
                inline=True,
            )

            if roles:
                embed.colour = next(
                    filter(lambda role: role.colour, roles), embed
                ).colour
                roles = [
                    role.mention
                    for role in roles
                    if role.id != context.interaction.guild_id
                ]
                embed.add_field(
                    name=context.locale.get("commands.user.info.fields.roles.name"),
                    value=(
                        context.locale.get(
                            "commands.user.info.fields.roles.sliced",
                            {"roles": ", ".join(roles[:5]), "sliced": len(roles) - 5},
                        )
                        if len(roles) > 5
                        else ", ".join(roles)
                        or context.locale.get("commands.user.info.fields.roles.none")
                    ),
                )

        return await context.create_response(embed=embed)
