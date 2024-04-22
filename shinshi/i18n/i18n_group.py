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

import logging
from dataclasses import dataclass, field
from typing import Any

_LOGGER = logging.getLogger("shinshi.i18n")
_ARGUMENTS_SENTINEL: dict[str, Any] = {}


@dataclass
class I18nGroup:
    name: str
    value: dict[str, str | tuple[str, ...] | I18nGroup] = field(default_factory=dict)

    def __find_value_in_group(
        self, sub_keys: list[str]
    ) -> str | tuple[str, ...] | None:
        current_group: I18nGroup = self
        for sub_key in sub_keys[:-1]:
            group = current_group.value.get(sub_key)
            if not isinstance(group, I18nGroup):
                return None
            current_group = group
        value: str | tuple[str, ...] | I18nGroup | None = current_group.value.get(
            sub_keys[-1]
        )
        return None if isinstance(value, I18nGroup) else value

    def __get_value_by_key(
        self,
        key: str,
    ) -> str | tuple[str, ...] | None:
        return self.__find_value_in_group(key.split("."))

    def __resolve_key(
        self,
        key: str,
        arguments: dict[str, Any],
    ) -> str | tuple[str, ...] | None:
        value = self.__get_value_by_key(key)
        if value is None:
            return key
        return value if isinstance(value, tuple) else value.format(**arguments)

    def get(
        self,
        key: str,
        arguments: dict[str, Any] | None = None,
    ) -> str:
        if arguments is None:
            arguments = _ARGUMENTS_SENTINEL
        try:
            value: str | tuple[str, ...] | None = self.__resolve_key(key, arguments)
            if not isinstance(value, str):
                _LOGGER.warning("failed to resolve i18n-key %s", key)
                return key
            return value
        except Exception as exception:
            _LOGGER.error(
                "Failed to resolve i18n-key %s in %s", key, self, exc_info=exception
            )
            return key

    def get_list(
        self, key: str, arguments: dict[str, Any] | None = None
    ) -> tuple[str, ...]:
        if arguments is None:
            arguments = _ARGUMENTS_SENTINEL
        try:
            value: str | tuple[str, ...] | None = self.__get_value_by_key(key)
            if not value:
                _LOGGER.warning("failed to resolve list-type i18n-key %s", key)
                return (key,)
            return tuple(item.format(**arguments) for item in value)
        except Exception as exception:
            _LOGGER.error(
                "Failed to resolve list-type i18n-key %s in %s",
                key,
                self,
                exc_info=exception,
            )
            return ()
