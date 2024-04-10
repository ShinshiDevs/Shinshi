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
FROM python:3.12.2-alpine
WORKDIR /usr/shinshi
COPY pyproject.toml .
COPY poetry.lock .
RUN python3.12 -m pip install poetry && \
    python3.12 -m poetry install
COPY . .
CMD ["poetry", "run", "python", "-OO", "-m", "shinshi"]
