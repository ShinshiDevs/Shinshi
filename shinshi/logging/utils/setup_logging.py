import logging
import logging.config
from pathlib import Path

from shinshi.data.data_provider import DataProvider


def setup_logging(file_path: Path) -> logging.Logger:
    logging.config.dictConfig(DataProvider.load_file(file_path))
    return logging.getLogger("shinshi")
