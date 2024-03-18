from dataclasses import dataclass
from typing import Dict

from hikari.locales import Locale

from shinshi.i18n import I18nProvider


@dataclass
class Translatable:
    i18n_key: str

    def translate(self, i18n_provider: I18nProvider) -> Dict[Locale, str]:
        translated: Dict[Locale, str] = {}
        for name in i18n_provider.locales.keys():
            i18n_provider.get(self.i18n_key, language=name)
        return translated
