import logging
import sys

from shinshi import LOGGER
from shinshi.aio.loop import create_loop
from shinshi.constants import dotenv_file, logging_dir
from shinshi.dotenv import load_dotenv
from shinshi.logging.utils import configure_logging

configure_logging(logging_dir / "configuration.yaml")
load_dotenv(dotenv_file)

if __name__ == '__main__':
    logger: logging.Logger = LOGGER.getChild("runtime")
    try:
        from shinshi import runtime

        logger.info("Starting...")
        runtime.run(create_loop())
    except KeyboardInterrupt:
        sys.exit(0)
else:
    sys.exit(0)
