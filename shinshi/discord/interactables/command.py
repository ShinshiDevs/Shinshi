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
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass, field
from typing import Any

from hikari.permissions import Permissions

from shinshi.discord.interactables.group import Group
from shinshi.discord.interactables.hooks import Hook
from shinshi.discord.interactables.interactable import Interactable
from shinshi.discord.interactables.options.option import Option
from shinshi.discord.models.translatable import Translatable


@dataclass(kw_only=True, slots=True)
class Command(Interactable):
    name: str
    description: Translatable | str | None = None

    group: Group | None
    sub_group: str | None

    default_member_permissions: Permissions
    is_dm_enabled: bool
    is_nsfw: bool

    options: Sequence[Option]
    hooks: Sequence[Hook]

    autocompletes: dict[str, Callable[..., Awaitable[Any]]] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        if self.group:
            if self.sub_group:
                sub_group: Group = self.group.sub_groups.setdefault(
                    self.sub_group, Group(name=self.sub_group)
                )
                sub_group.commands[self.name] = self
            else:
                self.group.commands[self.name] = self

    @property
    def qualname(self) -> str:
        parts = [getattr(self.group, "name", None), self.sub_group, self.name]
        return " ".join(filter(None, parts))

    def autocomplete(self, argument: str) -> None:
        def _(func: Callable[..., Awaitable[Any]]) -> None:
            self.autocompletes[argument] = func
