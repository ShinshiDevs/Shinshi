from datetime import datetime, timedelta
from typing import Literal


def format_datetime(
    time: datetime | timedelta,
    style: Literal["t", "T", "d", "D", "f", "F", "R"] | None = None,
) -> str:
    if isinstance(time, timedelta):
        time = datetime.now() + time
    assert isinstance(time, datetime)
    if style is not None:
        return f"<t:{int(time.timestamp())}:{style}>"
    return f"<t:{int(time.timestamp())}>"
