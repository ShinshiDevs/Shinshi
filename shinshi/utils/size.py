from cmath import log

size_units: tuple[str, ...] = ("B", "KB", "MB", "GB")


def humanize_size(input_size: int):
    if input_size == 0:
        return "0 B"

    index: int = int(log(input_size, 1024).real)
    base: int = pow(1024, index)
    size: int = round(input_size / base, 2)

    return f"{size} {size_units[index]}"
