import traceback


def format_exception(exception: Exception) -> str:
    formatted_string = "".join(traceback.format_exception(exception))
    return formatted_string.rstrip()
