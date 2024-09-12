import os
import sys
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING

from colorlog import basicConfig

LOG_LEVELS: dict[str, int] = {
    "DEBUG": DEBUG,
    "INFO": INFO,
    "WARNING": WARNING,
    "ERROR": ERROR,
    "CRITICAL": CRITICAL,
}
LOG_COLORS: dict[str, str] = {
    "DEBUG": "purple",
    "INFO": "black",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "white,bg_red",
}


def setup_logging(
    level: int = INFO,
    format: str | None = None,
    log_colors: dict[str, str] = LOG_COLORS,
) -> None:
    args = sys.argv
    if "--log" in sys.argv:
        log_index = args.index("--log") + 1
        if log_index < len(args):
            level = LOG_LEVELS[args[log_index]]

    basicConfig(
        level=level,
        format=format or os.environ.get("SHINSHI_LOGGING_FORMAT", ""),
        log_colors=log_colors,
    )
