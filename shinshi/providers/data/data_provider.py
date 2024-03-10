import logging
import os
from glob import glob
from typing import Any, Dict

from yaml import CLoader, load

from shinshi.logging import LoggerFactory
from shinshi.sdk.lifecycle import IStartable


class DataProvider(IStartable):
    def __init__(
        self,
        path: os.PathLike,
    ) -> None:
        self.__logger: logging.Logger = LoggerFactory.create(DataProvider)
        self.__path: os.PathLike = path
        self.files: Dict[str, Dict[str, Any]] = {}

    async def start(self) -> None:
        files: Dict[str, Dict[str, Any]] = {}
        directory: str = str(self.__path)
        self.__logger.debug(f"Loading files from {directory}")
        for file_name in glob("*.yaml", root_dir=directory):
            name: str = os.path.splitext(file_name)[0]
            with open(os.path.join(directory, file_name), "rb") as stream:
                data: dict[str, Any] = load(stream, Loader=CLoader)
                if not isinstance(data, dict):
                    raise ValueError(
                        "The file at the specified path "
                        f"'{name}' is not a valid file."
                    )
                files[name] = data
        self.files = files
        self.__logger.info(f"Loaded {", ".join(list(self.files.keys()))} files")

    def get_file(self, file_name: str) -> Dict[str, Any] | None:
        return self.files.get(file_name)
