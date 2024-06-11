# Shinshi - A modern and user-friendly Discord bot designed to give you and your servers great functionality and stable performance.
# Copyright (C) 2024 Shinshi Developers Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from os import getenv
from pathlib import Path

from aurum.client import Client
from aurum.enum.sync_commands import SyncCommandsFlag
from dotenv.main import load_dotenv
from hikari.impl import GatewayBot

ROOT_CWD: Path = Path.cwd()

load_dotenv(override=True)

if not (token := getenv("SHINSHI_DISCORD_TOKEN")):
    raise RuntimeError(
        "Unable to retrieve a token, please ensure that the environment secrets are loaded correctly."
    )
bot: GatewayBot = GatewayBot(token)
client: Client = Client(bot, sync_commands=SyncCommandsFlag.DEBUG)

if __name__ == "__main__":
    client.commands.load_folder(ROOT_CWD / "shinshi" / "commands")
    bot.run()
