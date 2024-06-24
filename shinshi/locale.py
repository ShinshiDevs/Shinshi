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
from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from typing import Any


@dataclass
class Locale:
    name: str
    value: dict[str, Any]

    def get(self, key: str, **format: Any) -> str:
        value: dict[str, Any] | str | None = self.value
        for part in key.split("."):
            value = value.get(part)
            if not value:
                return key
            if isinstance(value, str):
                return value.format(**format) if format else value
        return key

    def get_seq(self, key: str, **format) -> Iterator[str | dict[str, Any]]:
        value: dict[str, Any] | str | None = self.value
        for part in key.split("."):
            value = value.get(part)
            if not value:
                return
            if isinstance(value, Sequence):
                for item in value:
                    yield (
                        item.format(**format)
                        if format and isinstance(item, str)
                        else item
                    )
        return
