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
from typing import Any, Dict

DOTENV_REGEX: re.Pattern = re.compile(
    r"^(?P<identifier>[A-Za-z_]+\w*)=(?P<value>[^#]+)(#.*)?$"
)


def parse_dotenv_file(file_path: os.PathLike) -> Dict[str, Any]:
    try:
        with open(file_path, "r", encoding="UTF-8") as file:
            for line in file:
                match: re.Match[str] | None = DOTENV_REGEX.match(line)
                if not match:
                    continue
                os.environ[match.group("identifier")] = (
                    match.group("value").strip().replace('"', "")
                )
        return dict(os.environ)
    except Exception as exception:
        print(f"Error while load .env file: {exception}")
        return {}
