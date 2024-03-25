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
import logging
from typing import Dict

GREY: str = "\033[90m"
RED: str = "\033[91m"
YELLOW: str = "\033[93m"
CYAN: str = "\033[96m"
BLUE: str = "\033[94m"
BOLD: str = "\033[1m"
RESET: str = "\033[0m"


class ColoredFormatter(logging.Formatter):
    LEVELS: Dict[int, str] = {
        logging.INFO: BLUE,
        logging.DEBUG: GREY,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: RED,
    }

    def format(self, record: logging.LogRecord) -> str:
        record.levelname = (
            f"{self.LEVELS.get(record.levelno, '')}{record.levelname}{RESET}"
        )
        record.name = f"{CYAN}{BOLD}{record.name}{RESET}"
        return super().format(record)
