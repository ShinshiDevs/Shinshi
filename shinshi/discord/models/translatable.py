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
        for locale, _ in i18n_provider.locales.items():
            translated[locale.name] = i18n_provider.get(self.i18n_key, locale=locale)
        self.fallback = translated[Locale.EN_US]
        return translated
