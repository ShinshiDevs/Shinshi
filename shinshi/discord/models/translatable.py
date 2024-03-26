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
from dataclasses import dataclass
from typing import Dict, Tuple

from hikari.locales import Locale

from shinshi.i18n.i18n_provider import I18nProvider


@dataclass
class Translatable:
    key: str
    fallback: str | None = None

    def build(self, i18n_provider: I18nProvider) -> Tuple[str, Dict[str, str]]:
        languages: Dict[str, str] = {}
        for name, language in i18n_provider.languages.items():
            languages[name] = language.get(self.key)
        self.fallback = languages[Locale.EN_US]
        return self.fallback, languages
