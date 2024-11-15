from typing import Protocol

from shinshi.abc.services.iservice import IService


class IKernel(Protocol):
    async def start(self) -> None: ...

    async def stop(self) -> None: ...

    async def run(self) -> None: ...

    def get_service[T: IService](self, service_interface: type[T]) -> T:
        ...

    def register_service(self, service_interface: type[IService], service: IService) -> None:
        ...

    def remove_service(self, service_interface: type[IService]) -> None:
        ...
