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
import enum


class Colour(int, enum.Enum):
    DARKER = 0x2B2D30
    DARK = 0x505359
    WHITE = 0xFBFDFF

    RED = 0xF05454
    YELLOW = 0xF0C454
    GREEN = 0x68E653
    BLUE = 0x54B8F0
    DARK_BLUE = 0x5464F0
    PURPLE = 0xBC65F1
    PINK = 0xF054A9
