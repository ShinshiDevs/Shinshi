import subprocess
import tomllib
from typing import Any

from shinshi.abc.models.version import VersionInfo


def get_version() -> VersionInfo:
    git_sha: str = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("ascii").strip()
    with open("pyproject.toml", "rb") as stream:
        data: dict[str, str] = tomllib.load(stream)
        project: str | dict[Any, Any] = data.get("project", {})
        if not isinstance(project, dict):
            return VersionInfo(version="0.0.0", git_sha=git_sha)
        version: str = project.get("version", "0.0.0")
    return VersionInfo(version=version, git_sha=git_sha)
