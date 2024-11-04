from typing import Protocol

from aurum.l10n import LocalizationProviderInterface

from shinshi.abc.services.iservice import IService


class II18nProvider(IService, LocalizationProviderInterface, Protocol): ...
