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
from datetime import datetime


def format_datetime(time: datetime, style: str | None = None) -> str:
    """Format datetime into discord timestamp string"""
    valid_styles = ["t", "T", "d", "D", "f", "F", "R"]
    if style and style not in ["t", "T", "d", "D", "f", "F", "R"]:
        raise ValueError(
            f"Invalid style passed. Valid styles: {' '.join(valid_styles)}"
        )
    if style:
        return f"<t:{int(time.timestamp())}:{style}>"
    return f"<t:{int(time.timestamp())}>"
