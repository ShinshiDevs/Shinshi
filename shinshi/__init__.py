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
import pathlib
from logging.config import dictConfig
from typing import Final, Sequence

import orjson

__all__: Sequence[str] = ()
__license__: Final[str] = "GPL-3.0"
__copyright__: Final[str] = "Copyright (C) 2024 Shinshi Developers Team"
__github_url__: Final[str] = "https://github.com/ShinshiDevs/Shinshi"
__support_url__: Final[str] = "https://discord.gg/3bXW7an2ke"

with open(pathlib.Path(os.getcwd(), "resources", "logging.json")) as stream:
    dictConfig(orjson.loads(stream.read()))
