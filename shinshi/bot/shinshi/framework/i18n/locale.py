from typing import Any

import attrs

from shinshi.abc.i18n.ilocale import ILocale

_EMPTY_SENTINEL: dict = {}


@attrs.define(eq=False, kw_only=True, slots=True, weakref_slot=False)
class Locale(ILocale):
    name: str = attrs.field(repr=True)
    data: dict[str, Any] = attrs.field(hash=False, repr=False)

    def get(self, key: str, formatting: dict[str, Any] | None = None) -> str:
        if formatting is None:
            formatting = _EMPTY_SENTINEL
        value = self.data
        for index in key.split("."):
            if not isinstance(value, dict):
                break
            value = value.get(index)
        if isinstance(value, str):
            return value.format(**formatting)
        return key

    def get_list(self, key: str, *formatting: dict[str, Any]) -> list[str]:
        value = self.data
        for index in key.split("."):
            if not isinstance(value, dict):
                break
            value = value.get(index)
        if isinstance(value, list):
            return (
                [str(item).format(**fmt) for item, fmt in zip(value, formatting)]
                if formatting
                else value
            )
        return []
