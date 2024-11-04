from pathlib import Path


def get_icon(*path: str) -> Path:
    return Path("resources/icons").joinpath(*path)
