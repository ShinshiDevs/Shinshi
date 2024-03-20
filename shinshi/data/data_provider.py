import logging
from glob import glob
from pathlib import Path
from typing import Any, Dict

import yaml

from shinshi import LOGGER
from shinshi.events import EventsMeta, event_listener
from shinshi.events.lifetime_events import StartingEvent


# TODO: it need to be more simple. It's just a loader for emojis.yaml.
#   Maybe we can load emojis.yaml in bot, instead of a big class `DataProvider`.
#   Like this is made in configure_logging.
class DataProvider(metaclass=EventsMeta):
    def __init__(
        self,
        data_dir: Path,
    ) -> None:
        self.__logger: logging.Logger = LOGGER.getChild("data_provider")
        self.__data_dir: Path = data_dir
        self.files: Dict[str, Dict[str, Any]] = {}

    @event_listener(StartingEvent)
    async def start(self) -> None:
        self.__logger.debug("loading files from %s", self.__data_dir)
        for file_name in glob("*.yaml", root_dir=self.__data_dir):
            file: Path = self.__data_dir / file_name
            with open(file, "rb") as stream:
                data: dict[str, Any] = yaml.load(stream, Loader=yaml.CLoader)
                if not isinstance(data, dict):
                    raise ValueError(
                        "The file at the specified path "
                        f"'{file.name}' is not a valid file."
                    )
            self.files[file.name.replace(file.suffix, "")] = data
        self.__logger.info("loaded %s files", ", ".join(list(self.files.keys())))

    def get_file(self, file_name: str) -> Dict[str, Any] | None:
        return self.files.get(file_name)

    @staticmethod
    def load_file(file_path: Path) -> Dict[str, Any]:
        if file_path.suffix != ".yaml":
            raise ValueError("This file is not a YAML file.")
        with open(file_path, "rb") as stream:
            data: dict[str, Any] = yaml.load(stream, Loader=yaml.CLoader)
            if not isinstance(data, dict):
                raise ValueError(
                    "The file at the specified path "
                    f"'{file_path.name}' is not a valid file."
                )
        return data
