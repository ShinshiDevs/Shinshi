import tomllib

with open("pyproject.toml", "rb") as stream:
    version = tomllib.load(stream)["project"]["version"]


def get_version() -> str:
    return version