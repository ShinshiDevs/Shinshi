from collections.abc import Sequence
from logging import Logger, getLogger
from os import PathLike
from pathlib import Path

from yaml import CLoader, load

from shinshi.abc.i18n.ilocale import ILocale
from shinshi.framework.i18n.locale import Locale

_DEFAULT_LANGUAGE: str = "en_GB"


class I18nProvider:
    __slots__: Sequence[str] = ("__logger", "base_path", "languages")

    def __init__(self, base_path: PathLike[str]) -> None:
        self.__logger: Logger = getLogger("shinshi.i18n")

        self.base_path: Path = Path(base_path)
        self.languages: dict[str, ILocale] = {}

    async def start(self) -> None:
        if not self.base_path.exists():
            raise SystemError("Base path is not existing")
        for file in self.base_path.glob("*.yaml"):
            locale: ILocale | None = self.load_locale(file)
            if locale is None:
                continue
            self.languages[locale.name] = locale
            self.__logger.debug("loaded %s locale", locale.name)
        self.__logger.info("started with %s languages", ", ".join(self.languages.keys()))

    async def stop(self) -> None:
        self.languages.clear()

    def get_locale(self, name: str) -> ILocale | None:
        return self.languages.get(name)

    def get_default_locale(self) -> ILocale:
        locale: ILocale | None = self.languages.get(_DEFAULT_LANGUAGE)
        if not locale:
            raise RuntimeError("Default locale is None")
        return locale

    def load_locale(self, file: Path) -> ILocale | None:
        try:
            with open(file, "rb") as stream:
                data: dict[str, str] | None = load(stream, Loader=CLoader)
                if not data:
                    self.__logger.warning("%s has no data to load, skip", file)
                    return
                return Locale(name=data["name"], data=data)
        except TypeError as error:
            self.__logger.warning("cannot load %s due syntax error: %s", file, error, exc_info=error)
        except Exception as error:
            self.__logger.warning("cannot load %s due unexpected error: %s", file, error, exc_info=error)
        return
