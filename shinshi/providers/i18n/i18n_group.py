from __future__ import annotations as _

from dataclasses import dataclass, field
from typing import Dict, Sequence, Any, Tuple

_ARGUMENTS_SENTINEL: Dict[str, Any] = {}


@dataclass
class I18nGroup:
    name: str
    value: Dict[str, str | I18nGroup | Tuple[str, ...]] | None = field(default_factory=dict)

    def get(self, key: str, arguments: Dict[str, Any] | None = None) -> str:
        if arguments is None:
            arguments = _ARGUMENTS_SENTINEL
        value = self.__resolve_key(key, arguments)
        return value if isinstance(value, str) else key

    def get_list(
        self,
        key: str,
    ) -> Tuple[str, ...]:
        value = self.__resolve_key(key, _ARGUMENTS_SENTINEL)
        return value if isinstance(value, tuple) else ()

    def __resolve_key(
        self, key: str, arguments: Dict[str, Any] | None = None
    ) -> str | Tuple[str, ...] | None:
        value: Sequence[str] | str | None = self.__get_value_by_key(key)
        if value is None:
            return key
        return value if isinstance(value, tuple) else value.format(**arguments)

    def __find_value_in_group(self, sub_keys: Sequence[str]) -> str | Tuple[str, ...] | None:
        for sub_key in sub_keys[:-1]:
            current_group: I18nGroup = self.value.get(sub_key)
            if not isinstance(current_group, type(self)):
                return None
        value: str | Tuple[str, ...] | None = self.value.get(sub_keys[-1])
        return None if isinstance(value, type(self)) else value

    def __get_value_by_key(self, key: str) -> str | Tuple[str, ...] | None:
        return self.__find_value_in_group(
            key.split(".")
        )
