from typing import Protocol

from shinshi.abc.services.iservice import IService


class IHTTPService(IService, Protocol): ...
