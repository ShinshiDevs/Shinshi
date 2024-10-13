import os
from collections.abc import Sequence
from logging import Logger, getLogger
from pathlib import Path
from typing import Any

from aurum.l10n import LocalizationProviderInterface, Localized
from hikari.interactions import CommandInteraction, ComponentInteraction
from yaml import CLoader, load

from shinshi.i18n.types import Locale

_DEFAULT_LANGUAGE: str = "en_GB"


class I18nProvider(LocalizationProviderInterface):
    __slots__: Sequence[str] = ("__logger", "directory", "languages")

    def __init__(self, directory: os.PathLike[str]) -> None:
        self.__logger: Logger = getLogger(__name__)

        self.directory: os.PathLike[str] = directory
        self.languages: dict[str, Locale] = {}

    async def start(self) -> None:
        directory: os.PathLike[str] = self.directory
        if not isinstance(self.directory, Path):
            directory = Path(directory)
        for file in directory.glob("*.yaml"):
            name: str = file.name.split(".")[0]
            with open(file, "r", encoding="UTF-8") as buffer:
                data: dict[str, Any] = load(buffer, Loader=CLoader) or {}
                self.languages[name] = Locale(name=name, value=data)
        self.__logger.info(
            "started with %s languages",
            ", ".join(self.languages.keys()),
        )

    def build_localized(self, value: Localized) -> dict[Locale | str, str]:
        key: str = value.value
        locales: dict[str, Locale] = self.languages.copy()
        value.fallback = locales.pop(_DEFAULT_LANGUAGE).get(key)
        value.value = {}
        for name, language in locales.items():
            value.value[name] = language.get(key)

    def get_locale(self, by: str | CommandInteraction | ComponentInteraction) -> Any:
        if not isinstance(by, str):
            by = str(by.locale or by.guild_locale).lower()
        return self.languages.get(by, self.languages[_DEFAULT_LANGUAGE])
