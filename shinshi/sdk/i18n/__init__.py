from __future__ import annotations

__all__: Sequence[str] = ("Locale", "I18nProvider")

from collections.abc import Sequence

from .i18n_provider import I18nProvider
from .locale import Locale
