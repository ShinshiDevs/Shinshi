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
import logging
import os
from pathlib import Path
from typing import Any

import orjson

from shinshi.i18n import I18nGroup


class I18nProvider:
    def __init__(self, base_directory: Path) -> None:
        self.__logger = logging.getLogger("shinshi.i18n")
        self.base_directory = base_directory
        self.languages: dict[str, I18nGroup] = {}

    @staticmethod
    def __build_map(file: Path) -> I18nGroup | None:
        with open(file, "rb") as stream:
            data: dict[str, Any] = orjson.loads(stream.read()) or {}
            if not isinstance(data, dict):
                raise ValueError("Not valid localization file")
        root_group = I18nGroup("root")
        nodes: list[tuple[I18nGroup, dict[str, Any]]] = [(root_group, data)]
        while nodes:
            parent_group, json = nodes.pop(0)
            for name, value in json.items():
                if isinstance(value, dict):
                    child_group = I18nGroup(name)
                    parent_group.value[name] = child_group
                    nodes.append((child_group, value))
                elif isinstance(value, list):
                    parent_group.value[name] = tuple(
                        filter(lambda item: isinstance(item, str), value)
                    )
                elif isinstance(value, str):
                    parent_group.value[name] = value
        return root_group

    async def start(self) -> None:
        self.__logger.debug("loading localizations from %s...", self.base_directory)
        for file in self.base_directory.glob("*.json"):
            language = self.__build_map(file)
            self.languages[os.path.splitext(file.name)[0]] = language
        self.__logger.info("loaded %s languages", ", ".join(self.languages.keys()))
