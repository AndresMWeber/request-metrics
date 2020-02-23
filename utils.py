from urllib.parse import urljoin
import asyncio
from aiohttp import ClientResponse
from functools import update_wrapper
from functools import wraps


class config:
    BASE_URL = 'https://api.passninja.com/v1/'
    PASSES = 'passes'
    PASSES_ENDPOINT = urljoin(BASE_URL, PASSES)
    PASS_PAYLOAD_FILE = './payload.json'
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


def log_start(url: str, verb: str, runs: int):
    print('Running {0} request to {API}{OK}{1}{END}{END} - {OK}{2}{END} time(s):'.format(
        verb,
        url,
        runs,
        END=bcolors.ENDC,
        API=bcolors.OKBLUE,
        OK=bcolors.UNDERLINE))


def log_end_response(response: ClientResponse) -> None:
    print('| {STATUS}\033[1m {} {END}{END} | - {TIME}{}{END}'.format(
        response.status,
        response.elapsed,
        END=bcolors.ENDC,
        TIME=bcolors.OKBLUE if response.elapsed < 1 else bcolors.OKGREEN if response.elapsed <= 3 else bcolors.WARNING if response.elapsed < 5 else bcolors.FAIL,
        STATUS=bcolors.OKBLUE if response.status == 200 else bcolors.FAIL),
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
