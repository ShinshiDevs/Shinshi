from hikari import GatewayBot

from shinshi.abc.models.version import VersionInfo
from shinshi.utils.version import get_version


class Bot(GatewayBot):
    version: VersionInfo = get_version()
