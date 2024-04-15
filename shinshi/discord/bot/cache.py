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
from hikari.impl import CacheImpl, CacheSettings, CacheComponents, GatewayBot


class Cache(CacheImpl):
    settings = CacheSettings(
        components=CacheComponents.ALL,
        max_messages=100,
        max_dm_channel_ids=0,
    )

    def __init__(self, app: GatewayBot) -> None:
        print("hi")
        super().__init__(app, self.settings)
