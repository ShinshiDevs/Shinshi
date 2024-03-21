from __future__ import annotations

from enum import Enum


class Locale(Enum):
    ID = "id"  # Indonesian
    DA = "da"  # Danish
    DE = "de"  # German
    EN_GB = "en-GB"  # English, UK
    EN_US = "en-US"  # English, US
    ES_ES = "es-ES"  # Spanish
    FR = "fr"  # French
    HR = "hr"  # Croatian
    IT = "it"  # Italian
    LT = "lt"  # Lithuanian
    HU = "hu"  # Hungarian
    NL = "nl"  # Dutch
    NO = "no"  # Norwegian
    PL = "pl"  # Polish
    PT_BR = "pt-BR"  # Portuguese, Brazilian
    RO = "ro"  # Romanian
    FI = "fi"  # Finnish
    SV_SE = "sv-SE"  # Swedish
    VI = "vi"  # Vietnamese
    TR = "tr"  # Turkish
    CS = "cs"  # Czech
    EL = "el"  # Greek
    BG = "bg"  # Bulgarian
    RU = "ru"  # Russian
    UK = "uk"  # Ukrainian
    HI = "hi"  # Hindi
    TH = "th"  # Thai
    ZH_CN = "zh-CN"  # Chinese, China
    JA = "ja"  # Japanese
    ZH_TW = "zh-TW"  # Chinese, Taiwan
    KO = "ko"  # Korean

    def __str__(self) -> str:
        return self.value

    @classmethod
    def convert(cls, name: str) -> Locale:
        return cls[name.upper()]
