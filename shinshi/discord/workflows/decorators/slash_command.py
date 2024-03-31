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
from typing import Any, Awaitable, Callable, Dict, Tuple

from hikari.commands import CommandType
from hikari.permissions import Permissions

from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows.interactables.commands import SlashCommand
from shinshi.discord.workflows.interactables.hook import Hook
from shinshi.discord.workflows.interactables.options import Option


def slash_command(
    name: str | None = None,
    description: Translatable | str | None = None,
    options: Tuple[Option, ...] | None = None,
    hooks: Tuple[Hook, ...] | None = None,
    default_member_permissions: Permissions | None = None,
    is_dm_enabled: bool | None = None,
    is_nsfw: bool | None = None,
) -> Callable[[Callable[[Any], Awaitable[Any]]], SlashCommand]:
    def decorator(func: Callable[[Any], Awaitable[Any]]) -> SlashCommand:
        kwargs: Dict[str, Any] = {}
        if description is not None:
            kwargs["description"] = description
        if options is not None:
            kwargs["options"] = options
        if hooks is not None:
            kwargs["hooks"] = hooks
        if default_member_permissions is not None:
            kwargs["default_member_permissions"] = default_member_permissions
        if is_dm_enabled is not None:
            kwargs["is_dm_enabled"] = is_dm_enabled
        if is_nsfw is not None:
            kwargs["is_nsfw"] = is_nsfw
        return SlashCommand(
            command_type=CommandType.SLASH,
            callback=func,
            name=name or func.__name__,
            **kwargs,
        )

    return decorator
