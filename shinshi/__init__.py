from logging import Logger, getLogger
from typing import Final, Sequence

from shinshi.constants import LOGGING_DIR
from shinshi.logging.utils import configure_logging

__all__: Sequence[str] = ("__copyright__", "__license__", "__github__", "__support__", "logger")

__copyright__: Final[str] = "Copyright (C) 2024-Present Shinshi Developers Team"
__license__: Final[str] = "GPL-3.0"

__github__: Final[str] = "https://github.com/ShinshiDevs/Shinshi"
__support__: Final[str] = "https://dsc.gg/shinshi"

configure_logging(LOGGING_DIR / "configuration.yaml")
logger: Logger = getLogger("shinshi")
