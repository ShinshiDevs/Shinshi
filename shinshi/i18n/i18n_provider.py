import logging
from glob import glob
from pathlib import Path
from typing import Dict, Any, List, Tuple, Sequence

from shinshi.data.data_provider import DataProvider
from shinshi.i18n.constants import DEFAULT_LANGUAGE
from shinshi.i18n.types import I18nGroup

_ARGUMENTS_SENTINEL: Dict[str, Any] = {}


class I18nProvider:
    def __init__(self, locales_dir: Path) -> None:
        self.__logger: logging.Logger = logging.getLogger("shinshi.i18n")
        self.__locales_dir: Path = locales_dir
        self.locales: Dict[str, I18nGroup] = {}

    async def start(self) -> None:
        if not self.__locales_dir.exists():
            raise RuntimeError("Locales directory doesn't exist or not detected.")
        self.__logger.debug(f"Loading localization files from {self.__locales_dir}")
        for file_name in glob("*.yaml", root_dir=self.__locales_dir):
            file: Path = self.__locales_dir / file_name
            self.locales[file.name] = self.__build_map(file)
        self.__logger.info(f"Loaded {", ".join(list(self.locales.keys()))} languages")

    @staticmethod
    def __build_map(file_path: Path) -> I18nGroup:
        data: Dict[str, Any] = DataProvider.load_file(file_path)
        root_group: I18nGroup = I18nGroup(name="root")
        nodes: List[Tuple[I18nGroup, Dict[str, str | I18nGroup | Tuple[str, ...]]]] = [(root_group, data)]
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

    def get(
        self,
        key: str,
        arguments: Dict[str, Any] | None = None,
        language: str | None = None
    ) -> str:
        if arguments is None:
            arguments = _ARGUMENTS_SENTINEL
        try:
            value: str | Any = self.__resolve_key(key, arguments, language)
            return value if isinstance(value, str) else key
        except Exception as exception:
            self.__logger.error(
                f"Failed to resolve i18n-key {key} in {language}",
                exc_info=exception
            )
            return key

    def get_list(
        self,
        key: str,
        language: str | None = None,
    ) -> Tuple[str, ...]:
        try:
            value: Tuple[str, ...] | Any = self.__resolve_key(key, _ARGUMENTS_SENTINEL, language)
            return value if isinstance(value, tuple) else ()
        except Exception as exception:
            self.__logger.error(
                f"Failed to resolve list-type i18n-key {key} in {language}",
                exc_info=exception
            )
            return ()

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
        language: str | None
    ) -> str | Tuple[str, ...] | None:
        sub_keys: Sequence[str] = key.split(".")
        language_map: I18nGroup | None = self.locales.get(language) if language else None
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
        language: str | None = None
    ) -> str | Tuple[str, ...] | None:
        value: str | Tuple[str, ...] | None = self.__get_value_by_key(key, language)
        if value is None:
            return key
        return value if isinstance(value, tuple) else value.format(**arguments)
