import logging
import sys
from os import environ
from pathlib import Path

from kanata import find_injectables, LifetimeScope
from kanata.catalogs import InjectableCatalog

from shinshi.framework.dotenv.utils import get_log_level
from shinshi.framework.environment import Environment
from shinshi.framework.dotenv import load_dotenv
from shinshi.framework.kernel import Kernel
from shinshi.framework.logging.formatters import ConsoleFormatter
from shinshi.sdk.aio import setup_event_policy, create_loop

if __name__ != "__main__":
    sys.exit(0)

# system environment
environment: Environment = Environment()
# loop
setup_event_policy()
create_loop()
# .env file
if environ.get("SHINSHI_ENVIRONMENT", "SYSTEM").upper() != "DOCKER":
    if load_dotenv(Path(environment.root_path, "app.env")) is False:
        raise RuntimeError(".env file is not loaded correctly")
# logging
stream_handler: logging.StreamHandler = logging.StreamHandler()
stream_handler.setFormatter(ConsoleFormatter("%(asctime)s %(name)-40s %(levelname)-20s %(message)s"))
logging.basicConfig(level=get_log_level(), handlers=[stream_handler])

registrations = find_injectables("shinshi")
catalog = InjectableCatalog(registrations)
scope = LifetimeScope(catalog)
instance = scope.resolve(Kernel)
