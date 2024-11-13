from typing import Any, Protocol

from shinshi.abc.services.iservice import IService


class IKernel(Protocol):
    async def start(self) -> None: ...

    async def stop(self) -> None: ...

    async def run(self) -> None: ...

    def get_service(
        self, service_interface: IService, default: Any | None = None
    ) -> IService | None: ...

    def register_service(
        self, service_interface: IService, service: object
    ) -> None: ...

    def remove_service(self, service_interface: IService) -> None: ...
