import os
from typing import Dict, Any

from shinshi.dotenv.parse import parse_dotenv_file


def load_dotenv(file_path: os.PathLike) -> Dict[str, Any] | None:
    if variables := parse_dotenv_file(file_path):
        for key, value in variables.items():
            os.environ.update({key: value})
        return variables
    return None
