import logging
from glob import glob
from pathlib import Path
from typing import Any, Dict

import yaml

from shinshi import LOGGER
from shinshi.events import StartingEvent, event_manager


class DataProvider:
    def __init__(
        self,
        data_dir: Path,
    ) -> None:
        self.__logger: logging.Logger = LOGGER.getChild("data_provider")
        self.__data_dir: Path = data_dir
        self.files: Dict[str, Dict[str, Any]] = {}

        event_manager.subscribe(StartingEvent, self.start)

    async def start(self) -> None:
        self.__logger.debug("loading files from %s", self.__data_dir)
        for file_name in glob("*.yaml", root_dir=self.__data_dir):
            file: Path = self.__data_dir / file_name
            self.files[
                file.name.replace(file.suffix, "")
            ] = DataProvider.load_file(file)
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
