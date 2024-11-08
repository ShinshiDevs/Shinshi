import asyncio
import contextlib
import time
from collections.abc import Sequence
from logging import Logger, getLogger

from shinshi.abc.services.iservice import IService


class Kernel:
    __slots__: Sequence[str] = ("__logger", "loop", "services", "started_services")

    def __init__(
        self, *services: IService, loop: asyncio.AbstractEventLoop | None = None
    ) -> None:
        self.__logger: Logger = getLogger("shinshi.kernel")

        self.loop: asyncio.AbstractEventLoop = loop or asyncio.get_running_loop()

        self.services: tuple[IService] = services
        self.started_services: list[IService] = []

    async def start(self) -> None:
        start_time: float = time.monotonic()
        services_count: int = len(self.services)

        for index, service in enumerate(self.services, start=1):
            self.__logger.debug(
                "starting service %s (%s/%s)",
                service.__class__.__qualname__,
                index,
                services_count,
            )
            try:
                await service.start()
            except Exception as error:
                self.__logger.error(
                    "failed to start service %s due to an unexpected error: %s",
                    service.__class__.__qualname__,
                    error,
                    exc_info=error,
                )
                continue
            self.started_services.append(service)

        self.__logger.info(
            "started services in %.2f seconds (%s/%s)",
            time.monotonic() - start_time,
            len(self.started_services),
            services_count,
        )

    async def stop(self) -> None:
        for service in reversed(self.started_services):
            self.__logger.debug("stopping service %s", service.__class__.__qualname__)
            with contextlib.suppress():
                await service.stop()

        self.started_services.clear()
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
