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
from pathlib import Path
from typing import Final

__all__ = (
    "__license__",
    "__copyright__",
    "__github_url__",
    "__support_url__",
    "__banner_extras__",
    "RESOURCES_DIR",
    "CONFIG_DIR",
    "IMAGES_DIR",
)

__license__: Final[str] = "GPL-3.0"
__copyright__: Final[str] = "Copyright (C) 2024 Shinshi Developers Team"
__github_url__: str = "https://github.com/ShinshiDevs/Shinshi"
__support_url__: str = "https://discord.gg/3bXW7an2ke"

__banner_extras__: dict[str, str] = {
    "shinshi_license": __license__,
    "shinshi_copyright": __copyright__,
    "shinshi_github_url": __github_url__,
    "shinshi_support_url": __support_url__,
}

RESOURCES_DIR = Path.cwd() / "resources"
CONFIG_DIR = Path.cwd() / "config"
IMAGES_DIR = RESOURCES_DIR / "images"
