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
from typing import Any

from shinshi.discord.constants import DEFAULT_LANGUAGE
from shinshi.i18n import I18nProvider


@dataclass(slots=True)
class Translatable:
    key: str | None = None

    fallback: str = ""
    translates: dict[str, Any] = field(default_factory=dict)

    def build(self, i18n_provider: I18nProvider) -> None:
        if self.key:
            for name, group in i18n_provider.languages.items():
                self.translates[name] = group.get(self.key)
            self.fallback = self.translates.get(DEFAULT_LANGUAGE, self.fallback)
        elif not self.fallback:
            raise ValueError(
                "Don't have key and fallback. Invalid translatable object."
            )
