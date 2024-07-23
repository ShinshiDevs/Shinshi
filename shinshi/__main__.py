# Shinshi  Copyright (C) 2024  Shinshi Developers Team
import os

from aurum.client import Client
from hikari.impl import GatewayBot

from shinshi.dotenv import load_dotenv
from shinshi.l10n import LocalizationProvider

if __name__ == "__main__":
    load_dotenv()

    bot: GatewayBot = GatewayBot(os.environ.get("SHINSHI_DISCORD_TOKEN", ""))
    client: Client = Client(bot, l10n=LocalizationProvider("i18n"))

    bot.ruin()
