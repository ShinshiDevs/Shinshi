import asyncio
import logging
from os import environ

from shinshi.constants import logging_dir, dotenv_file, resources_dir
from shinshi.data.data_provider import DataProvider
from shinshi.dotenv import load_dotenv
from shinshi.http import HttpPoolClient
from shinshi.i18n import I18nProvider
from shinshi.logging.utils import setup_logging

logger: logging.Logger = setup_logging(logging_dir / "configuration.yaml")
load_dotenv(dotenv_file) if environ.get("SHINSHI_ENVIRONMENT", "SYSTEM").upper != "DOCKER" else None

http_pool_client: HttpPoolClient = HttpPoolClient()
i18n_provider: I18nProvider = I18nProvider(resources_dir / "i18n")
data_provider: DataProvider = DataProvider(resources_dir)


def run(loop: asyncio.AbstractEventLoop) -> None:
    logger.info("Starting Shinshi")
    # ignore this
    starting_tasks: List[Coroutine[[None], None]] = ()

    try:
        for task in
