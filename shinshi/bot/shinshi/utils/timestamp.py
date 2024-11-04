from datetime import datetime, timedelta
from typing import Literal, TypeVar

TimestampStyleT = TypeVar(
    "TimestampStyleT", bound=Literal["t", "T", "d", "D", "f", "F", "R"]
)


def format_timestamp(
    time: float | int,
    style: TimestampStyleT | None = None,
) -> str:
    if style is not None:
        return f"<t:{int(time)}:{style}>"
    return f"<t:{int(time)}>"


def format_datetime(
    time: datetime | timedelta,
    style: TimestampStyleT | None = None,
) -> str:
    if isinstance(time, timedelta):
        time = datetime.now() + time
    assert isinstance(time, datetime)
    return format_timestamp(time.timestamp(), style)
