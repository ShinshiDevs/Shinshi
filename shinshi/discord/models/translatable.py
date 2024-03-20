from dataclasses import dataclass
from typing import Dict

from hikari.locales import Locale

from shinshi.i18n import I18nProvider


@dataclass
class Translatable:
    i18n_key: str
    fallback: str | None = None

    def translate(self, i18n_provider: I18nProvider) -> Dict[str, str]:
        translated: Dict[str, str] = {}
        for name in i18n_provider.locales.keys():
            translated[Locale[name].value] = i18n_provider.get(self.i18n_key, locale=name)
        self.fallback = translated[Locale.EN_US]
        return translated
