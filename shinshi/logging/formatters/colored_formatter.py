import logging
from typing import Dict

from shinshi.logging.constants import RED, YELLOW, BLUE, CYAN, GREY, BOLD, RESET


class ColoredFormatter(logging.Formatter):
    LEVELS: Dict[int, str] = {
        logging.INFO: BLUE,
        logging.DEBUG: GREY,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: RED,
    }

    def format(self, record: logging.LogRecord) -> str:
        record.levelname = f"{self.LEVELS.get(record.levelno, '')}{record.levelname}{RESET}"
        record.name = f"{CYAN}{BOLD}{record.name}{RESET}"
        return super().format(record)
