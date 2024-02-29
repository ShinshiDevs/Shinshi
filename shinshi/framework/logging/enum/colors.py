from enum import Enum


class Colors(Enum):
    GREY = '\033[90m'

    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'

    BOLD = '\033[1m'
    ENDC = '\033[0m'
