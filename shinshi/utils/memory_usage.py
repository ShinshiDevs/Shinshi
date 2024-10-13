import os
import warnings

if os.name == "nt":
    try:
        import psutil  # pylint: disable=E0401
    except ImportError:
        psutil = None

    def get_memory_usage() -> int:
        if not psutil:
            warnings.warn("cannot get memory usage, because psutil is not installed")
            return 0
        process = psutil.Process(os.getpid())
        return process.memory_info().rss
else:
    from resource import RUSAGE_SELF, getrusage

    def get_memory_usage() -> int:
        return getrusage(RUSAGE_SELF).ru_maxrss
