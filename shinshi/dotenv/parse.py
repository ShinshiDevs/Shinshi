import os
import re
from typing import Any, Dict

DOTENV_REGEX: re.Pattern = re.compile(
    r"^(?P<identifier>[A-Za-z_]+\w*)=(?P<value>[^#]+)(#.*)?$"
)


def parse_dotenv_file(file_path: os.PathLike) -> Dict[str, Any]:
    try:
        with open(file_path, "r", encoding="UTF-8") as file:
            for line in file:
                match = DOTENV_REGEX.match(line)
                if not match:
                    continue
                os.environ[match.group("identifier")] = match.group("value").strip()
        return dict(os.environ)
    except Exception as exception:
        print(f"Error while load .env file: {exception}")
        return {}
