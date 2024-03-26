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

from hikari import CommandType, Permissions

from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows.interactables.commands.command import Command
from shinshi.discord.workflows.interactables.options.option import Option


@dataclass(kw_only=True)
class SlashCommand(Command):
    command_type = CommandType.SLASH

    description: Translatable | str = "No description"

    default_member_permissions: Permissions = Permissions.NONE
    is_dm_enabled: bool = False
    is_nsfw: bool = False

    options: Tuple[Option, ...] = field(default_factory=tuple)
