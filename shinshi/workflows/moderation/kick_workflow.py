# Copyright (C) 2024 Shinshi Developers Team
#
# This file is part of Shinshi.
#
# Shinshi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Shinshi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Shinshi.  If not, see <https://www.gnu.org/licenses/>.
import contextlib
from datetime import datetime

from hikari.commands import OptionType
from hikari.embeds import Embed
from hikari.files import Resourceish
from hikari.guilds import GatewayGuild
from hikari.interactions import InteractionMember
from hikari.permissions import Permissions
from hikari.users import User

from shinshi import IMAGES_DIR
from shinshi.discord.interactables.options import Option, StringOption
from shinshi.discord.interaction import InteractionContext
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows import Workflow
from shinshi.discord.workflows.decorators import command
from shinshi.ext.colour import Colour
from shinshi.workflows.moderation.hooks import kick_hook


class KickWorkflow(Workflow):
    @command(
        description=Translatable("commands.kick.description"),
        options=(
            Option(
                type=OptionType.USER,
                name="target",
                description=Translatable("commands.kick.arguments.target.description"),
            ),
            StringOption(
                type=OptionType.STRING,
                name="reason",
                description=Translatable("commands.kick.arguments.reason.description"),
                max_length=200,
                is_required=False,
            ),
            Option(
                type=OptionType.ATTACHMENT,
                name="attachment",
                description=Translatable(
                    "commands.kick.arguments.attachment.description"
                ),
                is_required=False,
            ),
        ),
        hooks=[
            kick_hook  # type: ignore  # TODO: the same history in shinshi/discord/interactables/command.py
        ],
        default_member_permissions=Permissions.KICK_MEMBERS,
    )
    async def kick(
        self,
        context: InteractionContext,
        target: User | InteractionMember,
        *,
        reason: str | None = None,
        attachment: Resourceish | None = None,
    ) -> None:
        reason = reason or context.i18n.get("special.not_specified")
        guild: GatewayGuild = context.interaction.get_guild()  # type: ignore
        try:
            await guild.kick(
                target,
                reason=f"[{context.interaction.user.global_name} (ID: {context.interaction.user.id})] {reason}",
            )
        except Exception as exception:
            raise exception
        else:
            await context.create_response(
                embed=(
                    Embed(
                        title=context.i18n.get("commands.kick.embed.author.title"),
                        colour=Colour.GREEN,
                        timestamp=datetime.now().astimezone(),
                    )
                    .set_author(
                        name=context.i18n.get("commands.kick.embed.author.author.name"),
                        icon=IMAGES_DIR / "moderation" / "success.webp",
                    )
                    .add_field(
                        name=context.i18n.get(
                            "commands.kick.embed.author.fields.reason"
                        ),
                        value=reason,
                    )
                )
            )
            with contextlib.suppress(Exception):
                embed = (
                    Embed(
                        title=context.i18n.get(
                            "commands.kick.embed.target.title",
                            {"guild": guild.name},
                        ),
                        colour=Colour.YELLOW,
                    )
                    .add_field(
                        name=context.i18n.get(
                            "commands.embed.target.fields.reason.name"
                        ),
                        value=reason,
                    )
                    .add_field(
                        name=context.i18n.get(
                            "commands.embed.target.fields.moderator.name"
                        ),
                        value=f"{context.interaction.user.mention}\n"
                        f"(ID: {context.interaction.user.id})",
                    )
                )
                if attachment:
                    embed.add_field(
                        name=context.i18n.get(
                            "commands.embed.target.fields.attachment.name"
                        ),
                        value=f"[{attachment.name[:-100]}]({attachment.url})",  # type: ignore
                    )
                await target.send(embed=embed)
