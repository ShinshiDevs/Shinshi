from __future__ import annotations as _

import logging
from typing import Any, Dict, Sequence, Tuple

_SENTINEL: Dict[str, Any] = {}


class I18nGroup:
    __slots__: Sequence[str] = ("__logger", "name", "value")

    def __init__(
        self,
        name: str,
        value: Dict[str, str | I18nGroup | Tuple[str, ...]] | None = None
    ) -> None:
        self.__logger: logging.Logger = logging.getLogger(f"shinshi.i18n.{name}")
        self.name: str = name
        self.value: Dict[str, str | I18nGroup | Tuple[str, ...]] | None = value if value is not None else _SENTINEL

    def get(self, key: str, arguments: Dict[str, Any] | None = None) -> str:
        if arguments is None:
            arguments = _SENTINEL
        value: str | Any = self.__resolve_key(key, arguments)
        return value if isinstance(value, str) else key

    def get_list(self, key: str) -> Tuple[str, ...]:
        value: Tuple[str, ...] | Any = self.__resolve_key(key, _SENTINEL)
        return value if isinstance(value, tuple) else ()

    def __resolve_key(
        self, key: str, arguments: Dict[str, Any] | None = None
    ) -> str | Tuple[str, ...] | None:
        value: str | Tuple[str, ...] | None = self.__get_value_by_key(key)
        if value is None:
            self.__logger.warning(f"Cannot resolve value of i18n-key: {key}")
            return key
        return value if isinstance(value, tuple) else value.format(**arguments)

    def __find_value_in_group(self, sub_keys: Sequence[str]) -> str | Tuple[str, ...] | None:
        for sub_key in sub_keys[:-1]:
            if not isinstance(self.value.get(sub_key), type(self)):
                return None
        value: str | Tuple[str, ...] | None = self.value.get(sub_keys[-1])
        return None if isinstance(value, type(self)) else value

    def __get_value_by_key(self, key: str) -> str | Tuple[str, ...] | None:
        return self.__find_value_in_group(key.split("."))
