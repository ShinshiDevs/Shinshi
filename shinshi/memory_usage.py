from collections.abc import Sequence
from datetime import datetime
from resource import RUSAGE_SELF, getrusage


class MemoryUsage:
    __slots__: Sequence[str] = ("records",)

    """Class for recording memory usage.

    Notes:
        - all memory recordings are in kilobytes.
        - works only on Unix-type systems.
    """

    def __init__(self) -> None:
        self.records: dict[datetime, int] = {}

    def record(self) -> tuple[datetime, int]:
        record = self.records[datetime.now()] = getrusage(
            RUSAGE_SELF
        ).ru_maxrss
        return record

    def get_heap_usage(self) -> tuple[datetime, int]:
        """Get heap usage from recordings.

        Returns:
            tuple[datetime, int]: heap record with datetime and RAM usage.
        """
        if not self.records:
            return self.record()
        heap_time: int = max(self.records, key=self.records.get)
        return heap_time, self.records[heap_time]
