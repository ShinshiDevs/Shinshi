from typing import Protocol
from shinshi.abc.services.iservice import IService


class IExtensionsService(IService, Protocol): ...
