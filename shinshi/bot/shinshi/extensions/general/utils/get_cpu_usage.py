import os


def get_cpu_usage() -> float:
    return (os.getloadavg()[0] / os.cpu_count() or 1) * 100
