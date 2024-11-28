import subprocess
from typing import Dict

import tomllib

from shinshi.abc.models.version import VersionInfo


def get_version() -> VersionInfo:
    with open("pyproject.toml", "rb") as stream:
        data: Dict[str, str] = tomllib.load(stream)
        version = data.get("project", {}).get("version", "0.0.0")
    git_sha: str = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("ascii").strip()
    return VersionInfo(version=version, git_sha=git_sha)
