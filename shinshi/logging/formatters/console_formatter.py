import logging
from typing import Dict

from shinshi.logging.enums.colors import Colors


class ConsoleFormatter(logging.Formatter):
    LEVELS: Dict[int, str] = {
        logging.INFO: Colors.BLUE,
        logging.DEBUG: Colors.GREY,
        logging.WARNING: Colors.YELLOW,
        logging.ERROR: Colors.RED,
        logging.CRITICAL: Colors.RED,
    }

    def __init__(
        self,
        fmt: str,
        date_format: str = "%Y-%m-%d %H:%M:%S",
        colors: bool = True
    ) -> None:
        super().__init__(fmt=fmt, datefmt=date_format)
        self.fmt: str = fmt
        self.date_format: str = date_format
        self.colors: bool = colors

    def format(self, record: logging.LogRecord) -> str:
        if self.colors:
            record.levelname = f"{self.LEVELS.get(record.levelno, '')}{record.levelname}{Colors.RESET}"
            record.name = f"{Colors.CYAN}{Colors.BOLD}{record.name}{Colors.RESET}"
        return super().format(record)
