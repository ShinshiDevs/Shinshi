import logging
import os
import pathlib
from typing import TYPE_CHECKING, Any

import orjson

from shinshi.i18n.i18n_group import I18nGroup

if TYPE_CHECKING:
    from logging import Logger


class I18nProvider:
    languages: dict[str, I18nGroup] = {}
    __slots__: tuple[str, ...] = ("__logger", "base_directory")

    def __init__(self, base_directory: str | os.PathLike) -> None:
        self.__logger: Logger = logging.getLogger("shinshi.i18n")
        self.base_directory: pathlib.Path = pathlib.Path(base_directory)

    @staticmethod
    def __build_map(file: pathlib.Path) -> I18nGroup:
        with open(file, "rb") as stream:
            data: dict[str, Any] = orjson.loads(stream.read()) or {}
            if not isinstance(data, dict):
                raise ValueError("Not valid localization file")
        root_group: I18nGroup = I18nGroup("root")
        nodes: list[tuple[I18nGroup, dict[str, Any]]] = [(root_group, data)]
        while nodes:
            parent_group, json = nodes.pop(0)
            for name, value in json.items():
                if isinstance(value, dict):
                    child_group = I18nGroup(name)
                    parent_group.value[name] = child_group
                    nodes.append((child_group, value))
                elif isinstance(value, list):
                    parent_group.value[name] = tuple(
                        filter(lambda item: isinstance(item, str), value)
                    )
                elif isinstance(value, str):
                    parent_group.value[name] = value
        return root_group

    async def start(self) -> None:
        self.__logger.debug("loading localizations from %s...", self.base_directory)
        for file in self.base_directory.glob("*.json"):
            self.languages[os.path.splitext(file.name)[0]] = self.__build_map(file)
        self.__logger.info("loaded %s languages", ", ".join(self.languages.keys()))
