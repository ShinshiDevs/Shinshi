from datetime import datetime, timedelta
from typing import Literal, TypeAlias

TimestampStyle: TypeAlias = Literal["t", "T", "d", "D", "f", "F", "R"]


def format_timestamp(
    time: float | int,
    style: TimestampStyle | None = None,
) -> str:
    if style is not None:
        return f"<t:{int(time)}:{style}>"
    return f"<t:{int(time)}>"


def format_datetime(
    time: datetime | timedelta,
    style: TimestampStyle | None = None,
) -> str:
    if isinstance(time, timedelta):
        time = datetime.now() + time
    assert isinstance(time, datetime)
    return format_timestamp(time.timestamp(), style)
