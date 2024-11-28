from collections.abc import Sequence

from shinshi.abc.models.version import VersionInfo
from shinshi.utils.version import get_version

__version_info__: VersionInfo = get_version()
__all__: Sequence[str] = ("__version_info__",)
