import logging
from typing import Final, Sequence

__all__: Sequence[str] = ("__copyright__", "__license__", "__github__", "__support__", "LOGGER")

__copyright__: Final[str] = "Copyright (C) 2024-Present Shinshi Developers Team"
__license__: Final[str] = "GPL-3.0"

__github__: Final[str] = "https://github.com/ShinshiDevs/Shinshi"
__support__: Final[str] = "https://dsc.gg/shinshi"

LOGGER: logging.Logger = logging.getLogger("shinshi")
