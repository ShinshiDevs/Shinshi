from typing import Protocol

from shinshi.abc.services.iservice import IService


class IConfigurationService(IService, Protocol): ...
