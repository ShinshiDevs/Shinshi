import logging
import logging.config
from os import PathLike

from yaml import CLoader, load


def setup_logging(
    *,
    config_file: PathLike[str] = "logging.yaml",
    verbose: bool = False,
) -> None:
    with open(config_file, "rb") as buffer:
        config: dict[str, str] = load(buffer, Loader=CLoader)
        if not config:
            if verbose:
                logging.warning("logging wasn't configured correctly because no config")
            config = {}
    logging.config.dictConfig(config)
