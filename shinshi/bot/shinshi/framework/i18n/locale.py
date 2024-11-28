from typing import Any, Dict

import attrs

_EMPTY_SENTINEL: Dict[str, Any] = {}


@attrs.define(eq=False, kw_only=True, slots=True, weakref_slot=False)
class Locale:
    name: str = attrs.field(repr=True)
    data: Dict[str, str] = attrs.field(hash=False, repr=False)

    def get(self, key: str, formatting: Dict[str, Any] | None = None) -> str:
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

    def get_list(self, key: str, *formatting: Dict[str, Any]) -> list[str]:
        value = self.data
        for index in key.split("."):
            if not isinstance(value, dict):
                break
            value = value.get(index)
        if isinstance(value, list):
            return [str(item).format(**fmt) for item, fmt in zip(value, formatting)] if formatting else value
        return []
