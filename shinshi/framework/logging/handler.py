import logging
from typing import Dict, Literal


class Formatter(logging.Formatter):
    def __init__(
        self,
        fmt: str | None,
        datefmt: str | None,
        style: Literal["%", "{", "$"] = '{'
    ) -> None:
        super().__init__()
        self.fmt: str | None = fmt
        self.datefmt: str = datefmt or "%d.%m.%y %H:%M:%S"
        self.style: str = style

    def format(self, record):
        formatter = logging.Formatter(
            fmt=self._format(record.levelno),
            datefmt=self.datefmt,
            style='{'
        )
        return formatter.format(record)

    def _format(self, log_level: int):
        formats: Dict[str, str] = {
            'LOG-LEVEL': {
                logging.DEBUG: '\x1b[38m',
                logging.INFO: '\x1b[34m',
                logging.WARNING: '\x1b[33m',
                logging.ERROR: '\x1b[31m',
                logging.CRITICAL: '\x1b[31m',
            }[log_level],
            'BLACK': '\x1b[30m',
            'RESET': '\x1b[0m',
            'BOLD': '\x1b[1m'
        }
        formatted: str = self.fmt
        for key, replacement in formats.items():
            if key in self.fmt:
                key = f"({key})"
                formatted.replace(key, formats[replacement])
        return formatted
