from aiohttp.client import ClientTimeout

DEFAULT_TIMEOUT: ClientTimeout = ClientTimeout(total=5)
