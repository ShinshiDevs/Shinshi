from typing import Protocol, Dict

from pathlib import Path

from shinshi.abc.i18n.ilocale import ILocale


class II18nProvider(Protocol):
    base_path: Path
    languages: Dict[str, ILocale]  # TODO: fix interface

    def get_locale(self, name: str) -> ILocale | None: ...

    def load_locale(self, file: Path) -> ILocale | None: ...

    def get_default_locale(self) -> ILocale: ...
