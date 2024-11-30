from enum import Enum

from hikari.locales import Locale as _Locale

LOCALE_MAP: dict[str, _Locale] = {"en_GB": _Locale.EN_GB, "ru": _Locale.RU}


class Locale(Enum):
    EN_GB = "en_GB"

    @classmethod
    def to_hikari(cls, locale_str: str) -> _Locale:
        return LOCALE_MAP.get(locale_str, _Locale.EN_GB)

    @classmethod
    def from_hikari(cls, hikari_locale: _Locale) -> str:
        for key, value in LOCALE_MAP.items():
            if value == hikari_locale:
                return key
        return "en_GB"
