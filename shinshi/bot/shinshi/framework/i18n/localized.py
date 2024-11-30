from __future__ import annotations

from collections.abc import Sequence
from typing import Self

from shinshi.abc.i18n.ilocale import ILocale


class Localized(str):
    __slots__: Sequence[str] = ("key", "fallback")

    def __new__(cls, key: str, fallback: str | None = None) -> Self:
        instance = super().__new__(cls, key)
        instance.key = key
        instance.fallback = fallback
        return instance

    def __repr__(self) -> str:
        return f"Localized(key={self.key!r}, fallback={self.fallback!r})"

    def __str__(self) -> str:
        return self.key

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Localized):
            return bool(self.key == other.key)
        return super().__eq__(other)

    def resolve(self, locale: ILocale) -> str:
        return locale.get(self.key) or self.fallback or self.key
