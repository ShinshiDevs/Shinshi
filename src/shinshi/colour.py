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
from enum import Enum


class Colour(int, Enum):
    RED = 0xF05454
    """Can be used for something * dangerous * like errors"""
    YELLOW = 0xF0C454
    """Can be used for warnings or something noncritical"""
    GREEN = 0x68E653
    """Can be used for something success"""
    BLUE = 0x54B8F0
    """Can be used for something with internal information"""
    BLURPLE = 0x5464F0
    """Can be used for something with external information, like user information"""
    PURPLE = 0xBC65F1
    """Can be used for system messages or developers information, like documentation"""
    PINK = 0xF054A9
    """Can be used for anything, not specified"""
