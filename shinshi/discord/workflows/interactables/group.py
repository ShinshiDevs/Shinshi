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
from typing import Dict

from hikari.permissions import Permissions
from hikari.snowflakes import Snowflake

from shinshi.discord.workflows.interactables.commands import SubCommand


@dataclass(kw_only=True)
class Group:
    name: str

    guild: Snowflake | str | int | None = None

    default_member_permissions: Permissions = Permissions.NONE
    is_dm_enabled: bool = False
    is_nsfw: bool = False

    commands: Dict[str, SubCommand | Dict[str, SubCommand]] = field(
        default_factory=dict
    )

    def get_command(
        self, subgroup_name: str | None, command_name: str
    ) -> SubCommand | None:
        command: SubCommand | Dict[str, SubCommand] | None = self.commands.get(
            command_name
        )
        if (subgroup_commands := self.commands.get(subgroup_name)) is not None:
            command = subgroup_commands.get(command_name)
        return command
