from pathlib import Path

ICON_PATH = Path.cwd() / "resource" / "icons"


def get_icon(*name: str) -> Path:
    name_list = list(name)
    name_list[-1] += ".webp"
    return Path(ICON_PATH, *name_list)
