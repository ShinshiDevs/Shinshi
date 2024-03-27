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
from typing import Dict

from hikari.commands import CommandChoice

from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows.interactables.options.choice import Choice
from shinshi.i18n.i18n_provider import I18nProvider


def convert_choice(i18n_provider: I18nProvider, choice: Choice) -> CommandChoice:
    name_localizations: Dict[str, str] | None = None
    if isinstance(choice.name, Translatable):
        name_localizations = choice.name.build(i18n_provider)
    return CommandChoice(
        name=getattr(choice.name, "fallback", choice.name),
        name_localizations=name_localizations,
        value=choice.value,
    )
