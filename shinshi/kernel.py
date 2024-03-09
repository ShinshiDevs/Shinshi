import asyncio
from typing import Sequence

from shinshi.logging import LoggerFactory
from shinshi.sdk.lifecycle import IStartable


class Kernel:
    __slots__: Sequence[str] = ("__loop", "__logger", "services")

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        services: Sequence[IStartable],
    ) -> None:
        self.__loop = loop
        self.__logger = LoggerFactory.create(Kernel)
        self.services = services

    def run(self):
        try:
            self.__logger.info("Starting services...")
            for service in self.services:
                self.__loop.run_until_complete(service.start())
            self.__loop.run_forever()
        except KeyboardInterrupt:
            self.__logger.info("Shutting down due to keyboard interrupt...")
            for service in self.services:
                self.__loop.run_until_complete(service.stop())
        finally:
            self.__loop.stop()
            self.__loop.close()
            self.__logger.info("Successful shutdown")
            asyncio.set_event_loop(None)
