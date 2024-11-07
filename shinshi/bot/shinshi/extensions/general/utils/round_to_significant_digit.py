from math import log10


def round_to_significant_digit(number: int) -> int:
    if number == 0:
        return 0
    rounding_base: int = 10 ** (int(log10(abs(number))) - 1)
    return round(number / rounding_base) * rounding_base
