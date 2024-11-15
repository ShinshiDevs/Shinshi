from collections.abc import Callable
from typing import Any

from shinshi.abc.services.iservice import IService


class IExtensionsService(IService):
    def inject_dependencies(self, func: Callable[..., None]) -> dict[str, Any]:
        ...
