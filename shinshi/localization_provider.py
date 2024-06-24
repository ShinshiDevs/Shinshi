# Shinshi - A modern and user-friendly Discord bot designed to give you and your servers great functionality and stable performance.
# Copyright (C) 2024 Shinshi Developers Team
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from collections.abc import Sequence
from logging import Logger, getLogger
from pathlib import Path
from typing import Any

from aurum import Localized
from aurum.l10n import LocalizationProviderInterface
from hikari import CommandInteraction, ComponentInteraction
from yaml import CLoader, load

from shinshi.locale import Locale


class LocalizationProvider(LocalizationProviderInterface):
    __slots__: Sequence[str] = ("__logger", "base_path", "languages")

    def __init__(self, base_path: Path) -> None:
        self.__logger: Logger = getLogger("shinshi.l10n")

        self.base_path: Path = base_path
        self.languages: dict[str, Locale] = {}

    async def start(self) -> None:
        for file in self.base_path.glob("*.yaml"):
            with open(file, "r", encoding="UTF-8") as stream:
                data: dict[str, Any] | None = load(stream, Loader=CLoader)
            if not isinstance(data, dict):
                self.__logger.warning("%s wasn't loaded correctly", file)
                data = {}
            name: str = file.name.split(".")[0]
            self.languages[name] = Locale(name=name, value=data)
        self.__logger.debug(
            "started successfully, loaded files: %s", ", ".join(self.languages.keys())
        )

    def build_localized(self, value: Localized) -> None:
        key: str = value.value
        languages: dict[str, Locale] = self.languages.copy()
        value.fallback = languages.pop("default").get(key)
        value.value = {}
        for name, locale in languages.items():
            value.value[name] = locale.get(key)

    def get_locale(self, by: str | CommandInteraction | ComponentInteraction) -> Any:
        name: str = by if isinstance(by, str) else str(by.locale or by.guild_locale)
        return self.languages.get(name, self.languages.get("default"))
