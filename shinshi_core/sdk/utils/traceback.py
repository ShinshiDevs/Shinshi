from traceback import format_exception


def get_traceback(exception: Exception) -> str:
    return "\n".join(
        format_exception(type(exception), exception, exception.__traceback__, 5, False)
    )
