import os
from logging.config import dictConfig

import orjson


def configure_logging(config: str | os.PathLike) -> None:
    with open(config, "r", encoding="UTF-8") as stream:
        dictConfig(orjson.loads(stream.read()))
