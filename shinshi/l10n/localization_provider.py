import os
from pathlib import Path
from typing import Any
from logging import Logger, getLogger

from yaml import load, CLoader
from aurum.l10n import LocalizationProviderInterface

from shinshi.l10n.locale import Locale


class LocalizationProvider(LocalizationProviderInterface):
    def __init__(self, directory: os.PathLike[str]) -> None:
        self.__logger: Logger = getLogger("shinshi.l10n")

        self.directory: os.PathLike[str] = directory
        self.languages: dict[str, Locale] = {}

    async def start(self) -> None:
        directory: os.PathLike[str] = self.directory
        if not isinstance(self.directory, Path):
            directory = Path(directory)
        for file in directory.glob("*.yaml"):
            name: str = file.name.split(".")[0]
            with open(file, "r") as buffer:
                data: dict[str, Any] = load(buffer, Loader=CLoader) or {}
                self.languages[name] = Locale(name=name, value=data)
        self.__logger.info(
            "started with %s languages",
            ", ".join(self.languages.keys()),
        )
