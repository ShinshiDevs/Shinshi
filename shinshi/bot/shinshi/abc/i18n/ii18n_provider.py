from typing import Protocol

from shinshi.abc.services.iservice import IService


class II18nProvider(IService, Protocol): ...
