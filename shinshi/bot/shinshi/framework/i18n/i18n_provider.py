import os
from logging import Logger, getLogger
from pathlib import Path

from yaml import CLoader, load

from shinshi.abc.i18n.ii18n_provider import II18nProvider
from shinshi.framework.i18n.locale import Locale


class I18nProvider(II18nProvider):
    def __init__(self, base_path: os.PathLike[str]) -> None:
        self.__logger: Logger = getLogger("shinshi.i18n")

        self.base_path: Path = Path(base_path)
        self.languages: dict[str, Locale] = {}

    async def start(self) -> None:
        if not self.base_path.exists():
            raise SystemError("Base path is not existing")
        for file in self.base_path.glob("*.yaml"):
            with open(file, "r", encoding="UTF-8") as stream:
                data: dict[str, str] | None = load(stream, Loader=CLoader)
                if not data:
                    self.__logger.warning("%s has no data to load, skip", file)
                    continue
                locale = self.languages[data["name"]] = Locale(
                    name=data["name"], data=data
                )
                self.__logger.debug("loaded %s locale", locale.name)
        self.__logger.info(
            "started with %s languages", ", ".join(self.languages.keys())
        )

    async def stop(self) -> None:
        self.languages = None
