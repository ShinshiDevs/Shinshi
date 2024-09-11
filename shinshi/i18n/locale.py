import attrs
from typing import Any


@attrs.define(hash=False, weakref_slot=False, kw_only=True)
class Locale:
    name: str = attrs.field(eq=False, repr=True)
    value: dict = attrs.field(eq=True, repr=False)

    def get(self, key: str, /, *formatting: dict) -> str | list[str]:
        value: dict | Any = self.value

        for sub in key.split("."):
            if isinstance(value, dict):
                value = value.get(sub)
                if value is None:
                    break
            if isinstance(value, str):
                for format in formatting:
                    value = value.format(**format)
                return value
            elif isinstance(value, list):
                return [item.format(**fmt) for item, fmt in zip(value, formatting)]

        return key
