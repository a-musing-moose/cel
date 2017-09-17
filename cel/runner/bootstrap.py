import json
import signal
import sys
from importlib import import_module


READ_TIMEOUT = 10  # Time in seconds to attempt to read from stdin
ENTRY_POINT_MODULE = 'app'
ENTRY_POINT = 'main'


def get_entry_point():
    try:
        module = import_module(ENTRY_POINT_MODULE)
    except ModuleNotFoundError as e:
        sys.stdout.write('{"error":"no entry point module found"}\n')
        sys.exit(1)

    try:
        return getattr(module, ENTRY_POINT)
    except AttributeError:
        sys.stdout.write('{"error":"entry point missing"}')
        sys.exit(1)


def timeout(sig_num, frame):
    """Handles exiting if a timeout alarm is raised"""
    sys.stdout.write('{"error":"stdin timeout"}')
    sys.exit(1)


def run():
    sys.path.insert(1, '/app')
    entry_point = get_entry_point()
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(READ_TIMEOUT)
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.stdout.write('{"error":"unable to read stdin"}')
        sys.exit(1)
    finally:
        signal.alarm(0)  # disable the alarm again

    try:
        json.dump(entry_point(payload), sys.stdout)
    except Exception as e:
        json.dump({"error": str(e)}, sys.stdout)
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    run()
