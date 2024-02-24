import logging
import traceback
from io import StringIO
from typing import Sequence


class ExternalLogFormatter:
    __slots__: Sequence[str] = ()

    @staticmethod
    def format(record: logging.LogRecord) -> str:
        with StringIO(record.getMessage()) as buffer:
            if record.exc_info:
                buffer.write("\n")
                if record.exc_text:
                    buffer.writelines((record.exc_text,))
                else:
                    traceback.print_exception(
                        record.exc_info[0],
                        record.exc_info[1],
                        record.exc_info[2],
                        None,
                        buffer,
                    )
            if record.stack_info:
                buffer.writelines((record.stack_info,))
            result = buffer.getvalue()
            return result if result.endswith("\n") else result[:-1]


DefaultInstance = ExternalLogFormatter()
