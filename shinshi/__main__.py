from shinshi.aio.loop import create_loop
from shinshi.constants import SECRETS_PATH, LOGGING_DIR
from shinshi.dotenv import load_dotenv
from shinshi.logging.utils import configure_logging

load_dotenv(SECRETS_PATH / "app.env")
configure_logging(LOGGING_DIR / "configuration.yaml")

if __name__ == '__main__':
    from shinshi import runtime

    runtime.run(create_loop())
