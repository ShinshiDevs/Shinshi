import logging
from typing import Dict

from shinshi.logging.console_colors import ConsoleColors


class ColoredFormatter(logging.Formatter):
    LEVELS: Dict[int, str] = {
        logging.INFO: ConsoleColors.BLUE,
        logging.DEBUG: ConsoleColors.GREY,
        logging.WARNING: ConsoleColors.YELLOW,
        logging.ERROR: ConsoleColors.RED,
        logging.CRITICAL: ConsoleColors.RED,
    }

    def format(self, record: logging.LogRecord) -> str:
        record.levelname = f"{self.LEVELS.get(record.levelno, '')}{record.levelname}{ConsoleColors.RESET}"
        record.name = f"{ConsoleColors.CYAN}{ConsoleColors.BOLD}{record.name}{ConsoleColors.RESET}"
        return super().format(record)
