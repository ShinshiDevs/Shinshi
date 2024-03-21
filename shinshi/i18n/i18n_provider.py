import logging
import os.path
from glob import glob
from pathlib import Path
from typing import Dict, Any, List, Tuple, Sequence

import yaml

from shinshi import LOGGER
from shinshi.discord.locale import Locale
from shinshi.events import event_listener, EventsMeta
from shinshi.events.lifetime_events import StartingEvent
from shinshi.exceptions.typing import AnyException
from shinshi.i18n.types import I18nGroup

DEFAULT_LANGUAGE: Locale = Locale.EN_US
_ARGUMENTS_SENTINEL: Dict[str, Any] = {}


class I18nProvider(metaclass=EventsMeta):
    def __init__(self, locales_dir: Path) -> None:
        self.__logger: logging.Logger = LOGGER.getChild("i18n")
        self.__locales_dir: Path = locales_dir
        self.locales: Dict[Locale, I18nGroup] = {}

    @event_listener(StartingEvent)
    async def start(self) -> None:
        self.__logger.debug("loading localization files from %s", self.__locales_dir)
        for file_name in glob("*.yaml", root_dir=self.__locales_dir):
            file: Path = self.__locales_dir / file_name
            self.locales[
                Locale.convert(os.path.splitext(file.name)[0])
            ] = self.__build_map(file)
        self.__logger.info(
            "loaded %s languages",
            ", ".join(locale.name for locale, _ in self.locales.items())
        )

    def get(
        self,
        key: str,
        arguments: Dict[str, Any] | None = None,
        locale: Locale | None = None
    ) -> str:
        if arguments is None:
            arguments = _ARGUMENTS_SENTINEL
        try:
            value: str | Any = self.__resolve_key(key, arguments, locale)
            return value if isinstance(value, str) else key
        except AnyException as exception:
            self.__logger.error(
                f"Failed to resolve i18n-key {key} in {locale}",
                exc_info=exception
            )
            return key

    def get_list(
        self,
        key: str,
        locale: Locale | None = None,
    ) -> Tuple[str, ...]:
        try:
            value: Tuple[str, ...] | Any = self.__resolve_key(key, _ARGUMENTS_SENTINEL, locale)
            return value if isinstance(value, tuple) else ()
        except AnyException as exception:
            self.__logger.error(
                f"Failed to resolve list-type i18n-key {key} in {locale}",
                exc_info=exception
            )
            return ()

    @staticmethod
    def __build_map(file_path: Path) -> I18nGroup:
        with open(file_path, "rb") as stream:
            data: dict[str, Any] = yaml.load(stream, Loader=yaml.CLoader)
            if not isinstance(data, dict):
                data = {}
        root_group: I18nGroup = I18nGroup(name="root")
        nodes: List[Tuple[I18nGroup, Dict[str, str | I18nGroup | Tuple[str, ...]]]] = [
            (root_group, data)
        ]
        while nodes:
            parent_group, data = nodes.pop(0)
            for name, value in data.items():
                if isinstance(value, dict):
                    child_group: I18nGroup = I18nGroup(name=name)
                    parent_group.value[name] = child_group
                    nodes.append((child_group, value))
                elif isinstance(value, (list, str)):
                    parent_group.value[name] = (
                        value if isinstance(value, str) else tuple(
                            _value for _value in value if isinstance(_value, str)
                        )
                    )
        return root_group

    @staticmethod
    def __find_value_in_group(
        group: I18nGroup,
        sub_keys: Sequence[str]
    ) -> str | Tuple[str, ...] | None:
        current_group: I18nGroup = group
        for sub_key in sub_keys[:-1]:
            current_group = current_group.value.get(sub_key)
            if not isinstance(current_group, I18nGroup):
                return None
        value: str | Tuple[str, ...] | I18nGroup | None = current_group.value.get(sub_keys[-1])
        return None if isinstance(value, I18nGroup) else value

    def __get_value_by_key(
        self,
        key: str,
        locale: Locale | None
    ) -> str | Tuple[str, ...] | None:
        sub_keys: Sequence[str] = key.split(".")
        language_map: I18nGroup | None = self.locales.get(locale) if locale else None
        has_checked_default: bool = False
        if not language_map:
            language_map = self.locales.get(DEFAULT_LANGUAGE)
            has_checked_default = True
        if not language_map:
            return None
        value = self.__find_value_in_group(language_map, sub_keys)
        if value is not None:
            return value
        if has_checked_default:
            return None
        language_map = self.locales.get(DEFAULT_LANGUAGE)
        return (
            self.__find_value_in_group(language_map, sub_keys)
            if language_map else None
        )

    def __resolve_key(
        self,
        key: str,
        arguments: Dict[str, Any],
        locale: Locale | None = None
    ) -> str | Tuple[str, ...] | None:
        value: str | Tuple[str, ...] | None = self.__get_value_by_key(key, locale)
        if value is None:
            return key
        return value if isinstance(value, tuple) else value.format(**arguments)
