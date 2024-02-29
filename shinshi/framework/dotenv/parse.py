from typing import Dict
from typing import Any

from .typing import T


def parse_dotenv_file(file_path: T) -> Dict[str, Any]:
    variables: Dict[str, Any] = {}
    try:
        with open(file_path, "r", encoding="UTF-8") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    variables[key.strip()] = value.strip()
        return variables
    except Exception as exception:
        print(f"Error while load .env file: {exception}")
        return {}
