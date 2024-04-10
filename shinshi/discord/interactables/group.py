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
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict, TypeVar

from hikari.permissions import Permissions

if TYPE_CHECKING:
    from shinshi.discord.interactables.command import Command as _Command

Command = TypeVar("Command", bound="_Command")


@dataclass(kw_only=True)
class Group:
    name: str

    default_member_permissions: Permissions = Permissions.NONE
    is_dm_enabled: bool = False
    is_nsfw: bool = False

    commands: Dict[str, Command] = field(default_factory=dict)
    sub_groups: Dict[str, SubGroup] = field(default_factory=dict)


@dataclass(kw_only=True)
class SubGroup:
    name: str
    commands: Dict[str, Command] = field(default_factory=dict)
