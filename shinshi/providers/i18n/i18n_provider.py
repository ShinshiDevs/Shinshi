import logging
import os
from glob import glob
from typing import Dict, Sequence, Any, Tuple, List

from yaml import CLoader, load

from shinshi.logging import LoggerFactory
from shinshi.providers.i18n import I18nGroup
from shinshi.sdk.lifecycle import IStartable

_DEFAULT_LANGUAGE: str = 'en_US'


class I18nProvider(IStartable):
    __slots__: Sequence[str] = ("__logger", "__path", "languages")

    def __init__(self, path: os.PathLike) -> None:
        self.__logger: logging.Logger = LoggerFactory.create(I18nProvider)
        self.__path: os.PathLike = path
        self.languages: Dict[str, I18nGroup] = {}

    async def start(self) -> None:
        languages: Dict[str, I18nGroup] = {}
        directory: str = str(self.__path)
        self.__logger.debug(f"Loading localization files from {directory}")
        for file_name in glob("*.yaml", root_dir=directory):
            name: str = os.path.splitext(file_name)[0]
            languages[name] = self.__build_map(os.path.join(directory, file_name), name)
        self.languages = languages
        self.__logger.info(f"Loaded {", ".join(list(self.languages.keys()))} languages")

    def get_language(self, language: str) -> I18nGroup:
        return self.languages.get(language, self.languages.get(_DEFAULT_LANGUAGE))

    @staticmethod
    def __build_map(file_path: str, name: str) -> I18nGroup:
        with open(file_path, "rb") as stream:
            data: Dict[str, Any] = load(stream, Loader=CLoader)
            if not isinstance(data, dict):
                raise ValueError(
                    f"The file at the specified path '{file_path}' is not a valid I18N Locale file."
                )
        root_group: I18nGroup = I18nGroup(name=name)
        nodes: List[Tuple[I18nGroup, Dict[str, str | I18nGroup | Tuple[str, ...]]]] = [(root_group, data)]
        while nodes:
            parent_group, data = nodes.pop(0)
            for locale_name, value in data.items():
                if isinstance(value, dict):
                    child_group = I18nGroup(name=locale_name)
                    parent_group.value[locale_name] = child_group
                    nodes.append((child_group, value))
                elif isinstance(value, (list, str)):
                    parent_group.value[locale_name] = (
                        value if isinstance(value, str) else tuple(
                            _value for _value in value if isinstance(_value, str)
                        )
                    )
        return root_group
