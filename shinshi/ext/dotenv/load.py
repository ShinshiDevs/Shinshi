import os
import re

DOTENV_REGEX = re.compile(r"^([A-Za-z_]+\w*)=([^#]+)(#.*)?$")


def load_dotenv(file_path: str | os.PathLike = ".env") -> None:
    with open(file_path, "r", encoding="UTF-8") as file:
        for line in file:
            match: re.Match[str] | None = DOTENV_REGEX.match(line)
            if match:
                os.environ[match.group(1)] = match.group(2).strip().replace('"', "")
