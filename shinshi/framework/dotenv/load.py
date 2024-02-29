from os import environ

from .parse import parse_dotenv_file
from .typing import T


def load_dotenv(file_path: T) -> bool:
    if variables := parse_dotenv_file(file_path):
        for key, value in variables.items():
            environ.update({key: value})
        return True
    return False
