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
from logging import getLogger
from logging.config import dictConfig
from pathlib import Path

import orjson

is_configured: bool = False

if is_configured is False:
    with open(Path(os.getcwd(), "resources", "logging.json"), "rb") as stream:
        dictConfig(orjson.loads(stream.read()))
    is_configured = True

logger = getLogger(__package__.split(".")[0])
