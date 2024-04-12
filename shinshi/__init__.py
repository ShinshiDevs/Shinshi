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
import platform
from logging.config import dictConfig
from pathlib import Path
from typing import Any, Dict, Final, Sequence

import orjson

__all__: Sequence[str] = (
    "__license__",
    "__copyright__",
    "__github_url__",
    "__support_url__",
    "__banner_extras__",
    "RESOURCES_DIR",
    "IMAGES_DIR",
)

__license__: Final[str] = "GPL-3.0"
__copyright__: Final[str] = "Copyright (C) 2024 Shinshi Developers Team"
__github_url__: Final[str] = "https://github.com/ShinshiDevs/Shinshi"
__support_url__: Final[str] = "https://discord.gg/3bXW7an2ke"

__banner_extras__: Dict[str, Any] = {
    "shinshi_license": __license__,
    "shinshi_copyright": __copyright__,
    "shinshi_github_url": __github_url__,
    "shinshi_support_url": __support_url__,
    "python_implementation": platform.python_implementation(),
    "python_version": platform.python_version(),
}

RESOURCES_DIR = Path.cwd() / "resources"
IMAGES_DIR = RESOURCES_DIR / "images"

with open(RESOURCES_DIR / "logging.json") as stream:
    dictConfig(orjson.loads(stream.read()))
