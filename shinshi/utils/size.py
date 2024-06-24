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
import math

size_suffixes: tuple[str, ...] = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")


def convert_size(size_bytes: float) -> tuple[float, str]:
    if size_bytes == 0:
        return 0, "B"
    exponent: int = int(math.floor(math.log(size_bytes, 1024)))
    divisor: float = math.pow(1024, exponent)
    size_value: float = round(size_bytes / divisor, 2)
    return size_value, size_suffixes[exponent]
