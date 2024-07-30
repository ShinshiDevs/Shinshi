import attrs
from typing import Any, overload


@attrs.define(hash=False, weakref_slot=False, kw_only=True)
class Locale:
    name: str = attrs.field(eq=False, repr=True)
    value: dict = attrs.field(eq=True, repr=False)

    @overload
    def get(self, key: str, format: dict) -> str: ...

    @overload
    def get(self, key: str, format: list[dict]) -> list[str]: ...

    def get(self, key: str, format: dict | list[dict]) -> str | list[str]:
        value: dict | Any = self.value
        formats: dict = format if isinstance(format, list) else [format]

        for sub, fmt in zip(key.split("."), formats):
            if isinstance(value, dict):
                value = value.get(sub)
                if value is None:
                    break
            if isinstance(value, str):
                return value.format(**fmt)
            elif isinstance(value, list):
                return [item.format(**fmt) for item in value if isinstance(item, str)]
            else:
                return value

        return key
