from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from typing import Any


@dataclass
class Locale:
    name: str
    value: dict[str, Any]

    def get(self, key: str, **format: Any) -> str:
        value: dict[str, Any] | str | None = self.value
        for part in key.split("."):
            value = value.get(part)
            if not value:
                return key
            if isinstance(value, str):
                return value.format(**format) if format else value
        return key

    def get_seq(self, key: str, **format) -> Iterator[str | dict[str, Any]]:
        value: dict[str, Any] | str | None = self.value
        for part in key.split("."):
            value = value.get(part)
            if not value:
                return
            if isinstance(value, Sequence):
                for item in value:
                    yield (
                        item.format(**format)
                        if format and isinstance(item, str)
                        else item
                    )
        return
