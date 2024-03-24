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
        record.levelname = f"{self.LEVELS.get(record.levelno, '')}{record.levelname}{RESET}"
        record.name = f"{CYAN}{BOLD}{record.name}{RESET}"
        return super().format(record)
