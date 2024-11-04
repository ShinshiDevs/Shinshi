import os

if os.name != "nt":
    import resource
else:
    resource = None  # pylint: disable=C0103


def get_memory_usage() -> int:
    if resource is not None:
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return 0
