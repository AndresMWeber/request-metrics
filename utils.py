from urllib.parse import urljoin
import asyncio
import json
from aiohttp import ClientResponse
from functools import update_wrapper
from functools import wraps

class config:
    ENDPOINT = urljoin('https://api.passninja.com/v1', 'passes')
    PAYLOAD_FILE = './payload_data.json'
    HEADER_FILE = './payload_headers.json'
    JSON_HEADER = {"Content-Type": "application/json"}


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Notifier(object):
    verbose: True

    @classmethod
    def emit(cls, *args, **kwargs):
        if cls.verbose:
            print(*args, **kwargs)

def dump_json (json_data):
    return '{JSON}{DATA}{END}'.format(DATA=json.dumps(json_data, indent=2, sort_keys=True), JSON=bcolors.OKBLUE, END=bcolors.ENDC)

def log_start(url: str, verb: str, runs: int):
    print('Running {0} request to {API}{OK}{1}{END}{END} - {OK}{2}{END} time(s):'.format(
        verb,
        url,
        runs,
        END=bcolors.ENDC,
        API=bcolors.OKBLUE,
        OK=bcolors.UNDERLINE))


def log_end_response(status: int, elapsed: float) -> None:
    print('| {STATUS}\033[1m {} {END}{END} | - {TIME}{}{END}'.format(
        status,
        elapsed,
        END=bcolors.ENDC,
        TIME=bcolors.OKBLUE if elapsed < 1 else bcolors.OKGREEN if elapsed <= 3 else bcolors.WARNING if elapsed < 5 else bcolors.FAIL,
        STATUS=bcolors.OKBLUE if status == 200 else bcolors.FAIL),
        flush=True)


def log_report(runs: int, runtimes: int) -> None:
    print('\n\nAverage run time was {OK}{0:.2f}s{END} over {GOOD}{1}{END} runs with {WARN}{2}{END} non-200 responses.'.format(
        sum(runtimes)/len(runtimes) if int(len(runtimes)) and runs else 0,
        len(runtimes),
        int(runs) - len(runtimes),
        OK=bcolors.OKGREEN,
        GOOD=bcolors.OKBLUE,
        WARN=bcolors.WARNING,
        END=bcolors.ENDC
    ))


def coro(f):
    f = asyncio.coroutine(f)

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(f(*args, **kwargs))
    return update_wrapper(wrapper, f)
