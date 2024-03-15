import sys

from shinshi import runtime
from shinshi.aio.loop import create_loop

if __name__ == '__main__':
    try:
        runtime.run(create_loop())
    except KeyboardInterrupt:
        sys.exit(0)
else:
    sys.exit(0)
