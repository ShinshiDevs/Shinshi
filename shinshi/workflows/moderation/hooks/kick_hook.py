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
from hikari.guilds import GatewayGuild, Role
from hikari.interactions import InteractionMember

from shinshi.discord.interactables.hooks import HookResult
from shinshi.discord.interaction import InteractionContext


async def kick_hook(context: InteractionContext) -> HookResult:
    target: InteractionMember = context.arguments["target"]
    guild: GatewayGuild = context.interaction.get_guild()  # type: ignore
    if not isinstance(target, InteractionMember):
        await context.send_warning(
            context.i18n.get("commands.kick.exceptions.target_is_user")
        )
        return HookResult(stop=True)
    if target.id == context.interaction.user.id:
        await context.send_warning(
            context.i18n.get("commands.kick.exceptions.cannot_kick_yourself")
        )
        return HookResult(stop=True)
    if target.id == context.bot.me.id:
        await context.send_warning(
            context.i18n.get("commands.kick.exceptions.bot_cannot_kick_yourself")
        )
        return HookResult(stop=True)
    if target_role := target.get_top_role():
        author_role: Role | None = context.interaction.member.get_top_role()  # type: ignore
        bot_role: Role | None = guild.get_my_member().get_top_role()  # type: ignore  # idk how to fix it, honestly
        if author_role and target_role.position >= author_role.position:
            await context.send_warning(
                context.i18n.get("commands.kick.exceptions.moderator_position_is_lower")
            )
            return HookResult(stop=True)
        if bot_role and target_role.position >= bot_role.position:
            await context.send_warning(
                context.i18n.get("commands.kick.exceptions.bot_position_is_lower")
            )
            return HookResult(stop=True)
    return HookResult()
