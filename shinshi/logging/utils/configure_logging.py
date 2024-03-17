import logging
import logging.config
from pathlib import Path
from typing import Any

import yaml

from shinshi.exceptions.typing import AnyException


def configure_logging(file: Path) -> None:
    try:
        with open(file, "rb") as stream:
            data: dict[str, Any] = yaml.load(stream, Loader=yaml.CLoader)
            logging.config.dictConfig(data)
    except AnyException:
        logging.basicConfig(level=logging.DEBUG)
