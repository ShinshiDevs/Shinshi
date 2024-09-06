import os

from colorlog import DEBUG, basicConfig

LOG_COLORS: dict[str, str] = {
    "DEBUG": "purple",
    "INFO": "thin",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "white,bg_red",
}


def setup_logging(
    level: int = DEBUG,
    format: str | None = None,
    log_colors: dict[str, str] = LOG_COLORS,
) -> None:
    basicConfig(
        level=level,
        format=format or os.environ.get("SHINSHI_LOGGING_FORMAT", ""),
        log_colors=log_colors,
    )
