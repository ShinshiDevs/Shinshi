import re
from typing import Iterable

from hikari.snowflakes import Snowflake


def find_emojis(string: str) -> Iterable[Snowflake]:
    for match in re.findall(r"<a?:\w+:(\d+)>|(\d+)", string):
        yield Snowflake(match[0] or match[1])
    return
