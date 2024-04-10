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
import os
from collections import deque
from logging import getLogger
from pathlib import Path
from typing import Any, Dict

import orjson

from shinshi.i18n import I18nGroup


class I18nProvider:
    def __init__(self, base_directory: Path) -> None:
        self.__logger = getLogger("shinshi.i18n")
        self.base_directory = base_directory
        self.languages: Dict[str, I18nGroup] = {}

    def __build_map(self, file: Path) -> I18nGroup | None:
        with open(file, "rb") as stream:
            try:
                data: Dict[str, Any] | Any = orjson.loads(stream.read()) or {}
                if not isinstance(data, dict):
                    raise ValueError("Not valid localization file")
            except Exception as exception:
                self.__logger.error(
                    "Cannot load localization file: %s", file, exc_info=exception
                )
                return
        root = I18nGroup("root")
        units = deque([(root, data)])
        while units:
            parent_group, current_data = units.popleft()
            for name, value in current_data.items():
                if isinstance(value, dict):
                    child_group = I18nGroup(name)
                    parent_group.value[name] = child_group
                    units.append((child_group, value))
                elif isinstance(value, list):
                    parent_group.value[name] = tuple(
                        filter(lambda item: isinstance(item, str), value)
                    )
                elif isinstance(value, str):
                    parent_group.value[name] = value
        return root

    async def start(self) -> None:
        self.__logger.debug("Starting...")
        if not self.base_directory.exists():
            raise RuntimeError(f"Cannot access {self.base_directory}")
        for file in self.base_directory.glob("*.json"):
            language = self.__build_map(file)
            self.languages[os.path.splitext(file.name)[0]] = language
        self.__logger.info("Loaded %s languages", ", ".join(self.languages.keys()))
