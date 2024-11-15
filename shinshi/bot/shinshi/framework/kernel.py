import asyncio
import contextlib
import time
from collections.abc import Sequence
from logging import Logger, getLogger

from shinshi.abc.kernel.ikernel import IKernel
from shinshi.abc.kernel.types.kernel_aware import KernelAware
from shinshi.abc.services.iservice import IService


class Kernel(IKernel):
    __slots__: Sequence[str] = ("__logger", "loop", "services")

    def __init__(self, loop: asyncio.AbstractEventLoop | None = None) -> None:
        self.__logger: Logger = getLogger("shinshi.kernel")
        self.loop: asyncio.AbstractEventLoop = loop or asyncio.get_running_loop()
        self.services: dict[type[IService], IService] = {}

    async def start(self) -> None:
        start_time: float = time.monotonic()

        started_services: int = 0
        services_count: int = len(self.services)

        for index, service in enumerate(self.services.values(), start=1):
            self.__logger.debug("starting service %s (%s/%s)", service.__class__.__qualname__, index, services_count)
            try:
                await service.start()
            except Exception as error:  # pylint: disable=W0718
                self.__logger.error(
                    "failed to start service %s due to an unexpected error: %s",
                    service.__class__.__qualname__,
                    error,
                    exc_info=error,
                )
                continue
            started_services += 1

        self.__logger.info(
            "started services in %.2f seconds (%s/%s)", time.monotonic() - start_time, started_services, services_count
        )

    async def stop(self) -> None:
        for service in reversed(self.services.values()):
            self.__logger.debug("stopping service %s", service.__class__.__qualname__)
            with contextlib.suppress():
                await service.stop()

        self.services.clear()
        self.__logger.info("stopped services successfully")

    async def run(self) -> None:
        await self.start()
        try:
            stop_event = asyncio.Event()
            self.__logger.info("ready")
            await stop_event.wait()
        except asyncio.CancelledError:
            self.__logger.info("shutting down due to cancelling...")
        except KeyboardInterrupt:
            self.__logger.info("shutting down due to keyboard interrupt...")
        finally:
            await self.stop()

    def get_service[T: IService](self, service_interface: type[T]) -> T:
        service: IService | None = self.services.get(service_interface)
        if service is None:
            raise RuntimeError(f"{service_interface.__name__} is not registred in Kernel")
        return service  # type: ignore

    def register_service(self, service_interface: type[IService], service: IService) -> None:
        if isinstance(service, KernelAware):
            service.set_kernel(self)
        self.services[service_interface] = service

    def remove_service(self, service_interface: type[IService]) -> None:
        self.services.pop(service_interface)
