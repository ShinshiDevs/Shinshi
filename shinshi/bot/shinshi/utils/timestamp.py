from datetime import UTC, datetime, timedelta
from typing import Literal, TypeAlias

TimestampStyle: TypeAlias = Literal["t", "T", "d", "D", "f", "F", "R"]


def format_timestamp(time: float | int, style: TimestampStyle | None = None) -> str:
    return f'<t:{int(time)}{f":{style}" if style else ""}>'


def format_datetime(time: datetime | timedelta, style: TimestampStyle | None = None) -> str:
    if isinstance(time, timedelta):
        time = datetime.now(UTC) + time
    return format_timestamp(time.timestamp(), style)
