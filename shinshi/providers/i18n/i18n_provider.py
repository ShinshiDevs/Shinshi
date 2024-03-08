import logging
import os
from glob import glob
from pathlib import Path
from typing import Dict, Sequence, Any, Tuple, List

from yaml import CLoader

from shinshi.providers.i18n import I18nGroup

_DEFAULT_LANGUAGE: str = 'en_US'


class I18nProvider:
    __slots__: Sequence[str] = ("__logger", "path", "languages")

    def __init__(self, path: os.PathLike) -> None:
        self.__logger: logging.Logger = LoggerFactory.create(I18nProvider)
        self.path: os.PathLike = path
        self.languages: Dict[str, I18nGroup] = {}

    async def start(self) -> None:
        languages: Dict[str, I18nGroup] = {}
        directory: str = str(self.path)
        self.__logger.debug(f"Loading localization files from {directory}")
        for file_name in glob(os.path.join(directory, "*.yaml")):
            languages[file_name] = self.__build_map(file_name)
        self.languages = languages
        self.__logger.info(f"Loaded {", ".join(list(self.languages.keys()))} languages")

    @staticmethod
    def __build_map(file_path: str) -> I18nGroup:
        with open(file_path, "rb") as stream:
            data: Dict[str, Any] = CLoader(stream).get_single_data()
            if not isinstance(data, dict):
                raise ValueError(
                    f"The file at the specified path '{file_path}' is not a valid I18N Locale file."
                )
        root_group: I18nGroup = I18nGroup(name=Path(file_path).name)
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
                            _value for _value in value if isinstance(_value, str))
                    )
        return root_group
