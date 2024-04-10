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

from hikari import Permissions
from shinshi.discord.interactables.command import Command
from shinshi.discord.interactables.group import Group
from shinshi.discord.interactables.hooks import HookResult
from shinshi.discord.interactables.options import Option
from shinshi.discord.models.translatable import Translatable


def command(
    name: str | None = None,
    description: Translatable | str | None = None,
    *,
    group: Group | None = None,
    sub_group: str | None = None,
    options: Tuple[Option, ...] | None = None,
    hooks: Tuple[Callable[[Any], Awaitable[HookResult]], ...] | None = None,
    default_member_permissions: Permissions | None = None,
    is_dm_enabled: bool | None = None,
    is_nsfw: bool | None = None,
    is_defer: bool | None = None,
    is_bound: bool | None = None,
    is_ephemeral: bool | None = None,
) -> Callable[[Callable[[Any], Awaitable[Any]]], Command]:
    def decorator(func: Callable[[Any], Awaitable[Any]]) -> Command:
        return Command(
            callback=func,
            **{
                name: argument
                for name, argument in dict(
                    name=name or func.__name__,
                    description=description,
                    group=group,
                    sub_group=sub_group,
                    options=options,
                    hooks=hooks,
                    default_member_permissions=default_member_permissions,
                    is_dm_enabled=is_dm_enabled,
                    is_nsfw=is_nsfw,
                    is_defer=is_defer,
                    is_bound=is_bound,
                    is_ephemeral=is_ephemeral,
                ).items()
                if argument is not None
            },
        )

    return decorator
