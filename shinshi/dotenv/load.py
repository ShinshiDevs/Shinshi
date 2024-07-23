# Shinshi  Copyright (C) 2024  Shinshi Developers Team
import os
import re
from typing import Any


def load_dotenv(
    file: os.PathLike[str] = ".env",
    *,
    regex: str = r"^([A-Z_]+_[A-Z_]+)=([A-Z_]+_[A-Z_]+)$",
) -> None:
    with open(file, "r", encoding="UTF-8") as buffer:
        variables: dict[str, Any] = re.findall(regex, buffer.read(), re.MULTILINE)
        os.environ.update(variables)
