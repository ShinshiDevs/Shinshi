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
from typing import TYPE_CHECKING, Tuple

from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows.interactables.commands.command import Command
from shinshi.discord.workflows.interactables.options.option import Option

if TYPE_CHECKING:
    from shinshi.discord.workflows.interactables.group import Group


@dataclass(kw_only=True)
class SubCommand(Command):
    description: Translatable | str | None = None

    group: "Group" = None
    sub_group: str | None = None

    options: Tuple[Option, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.sub_group:
            self.group.commands.setdefault(self.sub_group, {})[self.name] = self
        else:
            self.group.commands[self.name] = self
