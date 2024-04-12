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
import pathlib
import string
import sys
from typing import Any

import colorlog


def print_banner(
    banner_file: pathlib.Path,
    extra_args: dict[str, Any],
) -> None:
    args: dict[str, Any] = extra_args.copy()
    args.update(colorlog.escape_codes.escape_codes)
    with open(banner_file, "r", encoding="UTF-8") as stream:
        banner: str = string.Template(stream.read()).safe_substitute(args)
        sys.stdout.buffer.write(banner.encode("utf-8"))
        sys.stdout.flush()
