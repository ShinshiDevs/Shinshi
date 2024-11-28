from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Self
from shinshi.abc.i18n.ilocale import ILocale


class Localized(str):
    __slots__: Sequence[str] = ("key", "fallback")
    _is_localizable: bool = True

    def __new__(cls, key: str, fallback: str | None = None) -> Self:
        instance = super().__new__(cls, key)
        instance.key = key
        instance.fallback = fallback
        print(cls.__dir__)
        print(cls.resolve)
        return instance

    def __repr__(self) -> str:
        return f"Localized(key={self.key!r}, fallback={self.fallback!r})"

    def __str__(self) -> str:
        return self.key

    def resolve(self, locale: ILocale) -> str:
        return locale.get(self.key) or self.fallback or self.key

    def __eq__(self, other: Localized | str) -> bool:
        if isinstance(other, Localized):
            return self.key == other.key
        return super().__eq__(other)


def is_localized(value: Any) -> bool:
    return getattr(value, "_is_localizable", False)
