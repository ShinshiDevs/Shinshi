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

from hikari.commands import OptionType

from shinshi.discord.interactables.options.models.choice import Choice
from shinshi.discord.models.translatable import Translatable


@dataclass(kw_only=True, slots=True)
class Option:
    type: OptionType

    name: str
    description: Translatable | str | None = None

    choices: tuple[Choice, ...] = field(default_factory=tuple)

    is_required: bool = True
    is_autocomplete: bool = False
