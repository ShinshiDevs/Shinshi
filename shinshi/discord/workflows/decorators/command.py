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
from collections.abc import Awaitable, Callable
from typing import Any

from hikari.permissions import Permissions

from shinshi.discord.interactables.command import Command
from shinshi.discord.interactables.group import Group
from shinshi.discord.interactables.hooks.typing import HookT
from shinshi.discord.interactables.options import Option
from shinshi.discord.models.translatable import Translatable


def command(
    *,
    description: Translatable | str | None = None,
    name: str | None = None,
    group: Group | None = None,
    sub_group: str | None = None,
    options: tuple[Option, ...] = (),
    hooks: tuple[HookT, ...] = (),
    default_member_permissions: Permissions = Permissions.NONE,
    is_dm_enabled: bool = False,
    is_nsfw: bool = False,
    is_defer: bool = False,
    is_ephemeral: bool = False,
) -> Callable[[Callable[..., Awaitable[Any]]], Command]:
    def decorator(func: Callable[..., Awaitable[Any]]) -> Command:
        return Command(
            callback=func,
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
            is_ephemeral=is_ephemeral,
        )

    return decorator
