import logging
from typing import Dict

from ..enum import Colors


class ConsoleFormatter(logging.Formatter):
    LEVELS: Dict[int, str] = {
        logging.INFO: Colors.BLUE.value,
        logging.DEBUG: Colors.GREY.value,
        logging.WARNING: Colors.YELLOW.value,
        logging.ERROR: Colors.RED.value,
        logging.CRITICAL: Colors.RED.value
    }

    def __init__(
        self,
        fmt: str,
        datefmt: str = "%Y-%m-%d %H:%M:%S",
        colors: bool = True
    ) -> None:
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.fmt: str = fmt
        self.datefmt: str = datefmt
        self.colors: bool = colors

    def format(self, record: logging.LogRecord) -> str:
        if self.colors:
            record.levelname = f"{self.LEVELS.get(record.levelno, '')}{record.levelname}{Colors.ENDC.value}"
            record.name = f"{Colors.CYAN.value}{Colors.BOLD.value}{record.name}{Colors.ENDC.value}"
        else:
            pass
        return super().format(record)
