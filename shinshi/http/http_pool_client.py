import logging
from typing import Any, Dict

from aiohttp.client import ClientSession
from aiohttp.connector import BaseConnector, TCPConnector

from shinshi.http.constants import DEFAULT_TIMEOUT
from shinshi.http.utils.orjson import orjson_serialize


class HttpPoolClient:
    def __init__(self) -> None:
        self.__logger: logging.Logger = logging.getLogger("shinshi.http")
        self.connector: BaseConnector = TCPConnector()
        self.session: ClientSession = ClientSession(
            connector=self.connector,
            json_serialize=orjson_serialize,
            timeout=DEFAULT_TIMEOUT,
        )

    async def stop(self):
        self.__logger.debug("Closing session...")
        await self.session.close()
        self.__logger.debug("Successfully closed session")

    async def get(self, url: str, query_parameters: Dict[str, Any] | None = None) -> Any:
        async with self.session.get(url, params=query_parameters, timeout=DEFAULT_TIMEOUT) as response:
            return await response.json()
