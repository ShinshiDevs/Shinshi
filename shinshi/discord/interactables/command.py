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
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, Tuple

from hikari import Permissions

from shinshi.discord.interactables.group import Group, SubGroup
from shinshi.discord.interactables.hooks import HookResult
from shinshi.discord.interactables.interactable import Interactable
from shinshi.discord.interactables.options.option import Option
from shinshi.discord.models.translatable import Translatable


@dataclass(kw_only=True)
class Command(Interactable):
    name: str
    description: Translatable | str | None = None

    group: Group | None = None
    sub_group: str | None = None

    default_member_permissions: Permissions = Permissions.NONE
    is_dm_enabled: bool = False
    is_nsfw: bool = False

    options: Tuple[Option, ...] = field(default_factory=tuple)
    hooks: Tuple[Callable[[Any], Awaitable[HookResult]], ...] = field(
        default_factory=tuple
    )

    autocomplete: Dict[str, Callable[[Any], Awaitable[Any]]] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        if self.group:
            if self.sub_group:
                sub_group: SubGroup = self.group.sub_groups.setdefault(
                    self.sub_group, SubGroup(name=self.sub_group)
                )
                sub_group.commands[self.name] = self
            else:
                self.group.commands[self.name] = self

    @property
    def qualname(self) -> str:
        return (
            f"{getattr(self.group, "name", None)} " f"{self.sub_group} " f"{self.name}"
        ).replace("None ", "")

    def autocomplete(self, argument: str) -> None:
        def decorator(func: Callable[[Any], Awaitable[Any]]) -> None:
            self.autocomplete[argument] = func

        return decorator
