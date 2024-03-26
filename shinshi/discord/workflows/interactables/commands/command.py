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
from typing import Tuple

from hikari.commands import CommandType
from hikari.snowflakes import Snowflake

from shinshi.discord.workflows.interactables.hook import HookT
from shinshi.discord.workflows.interactables.interactable import Interactable


@dataclass(kw_only=True)
class Command(Interactable):
    command_type: CommandType
    name: str

    guild: Snowflake | str | int | None = None

    hooks: Tuple[HookT, ...] = field(default_factory=tuple)  # type: ignore
