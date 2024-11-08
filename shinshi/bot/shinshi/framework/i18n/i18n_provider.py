import os
from collections.abc import Sequence
from logging import Logger, getLogger
from pathlib import Path

from aurum.l10n import Localized
from hikari.interactions import BaseCommandInteraction
from yaml import CLoader, load

from shinshi.abc.i18n.ii18n_provider import II18nProvider
from shinshi.framework.i18n.locale import Locale

_DEFAULT_LANGUAGE: str = "en_GB"


class I18nProvider(II18nProvider):
    __slots__: Sequence[str] = ("__logger", "base_path", "languages")

    def __init__(self, base_path: os.PathLike[str]) -> None:
        self.__logger: Logger = getLogger("shinshi.i18n")

        self.base_path: Path = Path(base_path)
        self.languages: dict[str, Locale] = {}

    async def start(self) -> None:
        if not self.base_path.exists():
            raise SystemError("Base path is not existing")
        for file in self.base_path.glob("*.yaml"):
            locale: Locale = self.load_locale(file)
            self.languages[locale.name] = locale
            self.__logger.debug("loaded %s locale", locale.name)
        self.__logger.info(
            "started with %s languages", ", ".join(self.languages.keys())
        )

    async def stop(self) -> None:
        self.languages.clear()

    def load_locale(self, file: Path) -> Locale | None:
        try:
            with open(file, "rb") as stream:
                data: dict[str, str] | None = load(stream, Loader=CLoader)
                if not data:
                    self.__logger.warning("%s has no data to load, skip", file)
                    return
                return Locale(name=data["name"], data=data)
        except TypeError as error:
            self.__logger.warning(
                "cannot load %s due syntax error: %s", file, error, exc_info=error
            )
        except Exception as error:
            self.__logger.warning(
                "cannot load %s due unexpected error: %s", file, error, exc_info=error
            )
        return

    def build_localized(self, value: Localized) -> None:
        key: str = value.value
        value.value = {
            name: language.get(key)
            for name, language in self.languages.items()
            if name != _DEFAULT_LANGUAGE
        }
        value.fallback = self.languages[_DEFAULT_LANGUAGE].get(key)

    def get_locale(self, by: BaseCommandInteraction | str) -> Locale:
        return self.languages.get(
            by.locale if isinstance(by, BaseCommandInteraction) else by,
            self.languages[_DEFAULT_LANGUAGE],
        )
