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
from logging import getLogger
from typing import Any, Dict, Sequence, Tuple

_ARGUMENTS_SENTINEL: Dict[str, Any] = {}


@dataclass
class I18nGroup:
    __logger = getLogger("shinshi.i18n")

    name: str
    value: Dict[str, str | Tuple[str, ...] | I18nGroup] = field(default_factory=dict)

    def __find_value_in_group(
        self, sub_keys: Sequence[str]
    ) -> str | Tuple[str, ...] | None:
        current_group: I18nGroup = self
        for sub_key in sub_keys[:-1]:
            current_group = current_group.value.get(sub_key)
            if not isinstance(current_group, I18nGroup):
                return None
        value: str | Tuple[str, ...] | I18nGroup | None = current_group.value.get(
            sub_keys[-1]
        )
        return None if isinstance(value, I18nGroup) else value

    def __get_value_by_key(
        self,
        key: str,
    ) -> str | Tuple[str, ...] | None:
        return self.__find_value_in_group(key.split("."))

    def __resolve_key(
        self,
        key: str,
        arguments: Dict[str, Any],
    ) -> str | Tuple[str, ...] | None:
        value = self.__get_value_by_key(key)
        if value is None:
            return key
        return value if isinstance(value, tuple) else value.format(**arguments)

    def get(
        self,
        key: str,
        arguments: Dict[str, Any] | None = None,
    ) -> str:
        if arguments is None:
            arguments = _ARGUMENTS_SENTINEL
        try:
            value: str = self.__resolve_key(key, arguments)
            if not isinstance(value, str):
                self.__logger.warning("failed to resolve i18n-key %s", key)
                return key
            return value
        except Exception as exception:
            self.__logger.error(
                "Failed to resolve i18n-key %s in %s", key, self, exc_info=exception
            )
            return key

    def get_list(
        self, key: str, arguments: Dict[str, Any] | None = None
    ) -> Tuple[str, ...]:
        if arguments is None:
            arguments = _ARGUMENTS_SENTINEL
        try:
            value: Tuple[str, ...] = self.__get_value_by_key(key)
            if not value:
                self.__logger.warning("failed to resolve list-type i18n-key %s", key)
                return (key,)
            return tuple(item.format(**arguments) for item in value)
        except Exception as exception:
            self.__logger.error(
                "Failed to resolve list-type i18n-key %s in %s",
                key,
                self,
                exc_info=exception,
            )
            return ()
