from typing import Protocol

from shinshi.abc.services.iservice import IService


class IDatabaseService(IService, Protocol): ...
