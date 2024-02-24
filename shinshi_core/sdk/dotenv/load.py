from os import environ

from .parse import parse_dotenv_file


def load_dotenv(file_path: str) -> bool:
    env_variables: dict = parse_dotenv_file(file_path)
    if env_variables:
        for key, value in env_variables.items():
            environ[key] = value
        return True
    return False
