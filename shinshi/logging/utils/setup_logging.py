import logging
import logging.config
from pathlib import Path

from shinshi.data import DataProvider
from shinshi.exceptions.typing import AnyException


def setup_logging(file_path: Path) -> logging.Logger:
    try:
        logging.config.dictConfig(DataProvider.load_file(file_path))
    except AnyException:
        logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger("shinshi")
