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
from typing import Any, Awaitable, Callable, Tuple

from hikari.commands import CommandType
from hikari.permissions import Permissions

from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows.interactables.commands.slash_command import SlashCommand
from shinshi.discord.workflows.interactables.hook import Hook
from shinshi.discord.workflows.interactables.options.option import Option


def slash_command(
    name: str | None = None,
    description: Translatable | str | None = None,
    options: Tuple[Option, ...] | None = None,
    hooks: Tuple[Hook, ...] | None = None,
    default_member_permissions: Permissions | None = None,
    dm_enabled: bool | None = None,
    is_nsfw: bool | None = None,
) -> Callable[[Callable[[Any], Awaitable[Any]]], SlashCommand]:
    def decorator(func: Callable[[Any], Awaitable[Any]]) -> SlashCommand:
        return SlashCommand(
            command_type=CommandType.SLASH,
            callback=func,
            name=name or func.__name__,
            description=description,
            options=options,
            hooks=hooks,
            default_member_permissions=default_member_permissions,
            is_dm_enabled=dm_enabled,
            is_nsfw=is_nsfw,
        )

    return decorator
