from enum import Enum


class Colour(int, Enum):
    GREY = 0x505359
    """Should be used for default embeds."""
    YELLOW = 0xF0C454
    """Should be used for warnings and non-critical embeds."""
    RED = 0xF05454
    """Should be used for errors and critical embeds."""
