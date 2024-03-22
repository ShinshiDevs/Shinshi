from typing import Any, Dict

import yaml

from shinshi.constants import RESOURCES_DIR
from shinshi.http import HttpPoolClient
from shinshi.i18n import I18nProvider

with open(RESOURCES_DIR / "emojis.yaml", "rb") as stream:
    emojis: Dict[str, Any] = yaml.load(stream, Loader=yaml.CLoader)

http_pool_client: HttpPoolClient = HttpPoolClient()
i18n_provider: I18nProvider = I18nProvider(RESOURCES_DIR / "i18n")
