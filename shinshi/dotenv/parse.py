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
import re
from typing import Any

DOTENV_REGEX = re.compile(r"^([A-Za-z_]+\w*)=([^#]+)(#.*)?$")


def parse_dotenv_file(file_path: os.PathLike) -> dict[str, Any]:
    with open(file_path, "r", encoding="UTF-8") as file:
        for line in file:
            if match := DOTENV_REGEX.match(line):
                os.environ[match.group(1)] = match.group(2).strip().replace('"', "")
