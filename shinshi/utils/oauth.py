# Copyright (C) 2024 Shinshi Developers Team
#
# This file is part of Shinshi.
#
# Shinshi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Shinshi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Shinshi.  If not, see <https://www.gnu.org/licenses/>.
from hikari.permissions import Permissions
from hikari.snowflakes import Snowflakeish
from yarl import URL


def oauth_url(
    client_id: Snowflakeish,
    *,
    permissions: Permissions | None = None,
    guild: Snowflakeish | None = None,
    redirect_uri: str | None = None,
    scopes: list[str] | None = None,
    disable_guild_select: bool = False,
) -> str:
    base_url = URL("https://discord.com/oauth2/authorize").with_query(
        {"client_id": str(client_id)}
    )
    scopes = scopes or ["bot"]
    if scopes:
        scopes_param = "+".join(scopes) if scopes else "bot"
        base_url = base_url.update_query({"scope": scopes_param})
    if permissions:
        base_url = base_url.update_query({"permissions": permissions.value})
    if guild:
        base_url = base_url.update_query({"guild_id": str(guild.id)})
    if redirect_uri:
        base_url = base_url.update_query(
            {"response_type": "code", "redirect_uri": redirect_uri}
        )
    if disable_guild_select:
        base_url = base_url.update_query({"disable_guild_select": "true"})
    return str(base_url)
