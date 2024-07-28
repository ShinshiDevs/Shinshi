import os


def load_dotenv(file: os.PathLike[str] = ".env") -> None:
    with open(file, "r", encoding="UTF-8") as buffer:
        for line in buffer:
            if not line.startswith("#") and len(line.strip()) > 0:
                name, value = line.split("=", maxsplit=1)
                os.environ[name.strip()] = value.strip()
