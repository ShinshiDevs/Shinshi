import logging
import logging.config
import os
from typing import Any

import yaml

from shinshi.framework.exceptions.typing import AnyException

def configure_logging(file: os.PathLike) -> None:
    try:
        with open(file, "rb") as stream:
            data: dict[str, Any] = yaml.load(stream, Loader=yaml.CLoader)
            logging.config.dictConfig(data)
    except AnyException as exception:
        print(exception)
        logging.basicConfig(level=logging.DEBUG)
