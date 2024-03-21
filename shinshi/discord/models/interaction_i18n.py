from dataclasses import dataclass
from typing import Tuple, Dict, Any

from shinshi.discord.locale import Locale
from shinshi.i18n import I18nProvider


@dataclass
class InteractionLocale:
    i18n_provider: I18nProvider
    locale: Locale

    def get(self, key: str, arguments: Dict[str, Any] | None) -> str | None:
        return self.i18n_provider.get(key, arguments, locale=self.locale)

    def get_list(self, key: str) -> Tuple[str, ...] | None:
        return self.i18n_provider.get_list(key, locale=self.locale)
