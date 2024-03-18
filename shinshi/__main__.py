from shinshi.aio.loop import create_loop
from shinshi.constants import dotenv_file, logging_dir
from shinshi.dotenv import load_dotenv
from shinshi.logging.utils import configure_logging

load_dotenv(dotenv_file)
configure_logging(logging_dir / "configuration.yaml")

if __name__ == '__main__':
    from shinshi import runtime

    runtime.run(create_loop())
