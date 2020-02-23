#!/usr/bin/env python
import click
import json
from services import RequestService
from utils import log_start, log_end_response, log_report, config, coro


@click.command()
@click.option('--runs', '-r', default=10, help="Number of requests to run.")
@click.option('--url', '-u', default=config.PASSES_ENDPOINT, help="API Endpoint to post to.")
@click.option('--data', '-d', default=config.PASS_PAYLOAD_FILE, help="JSON data (if using POST).")
@click.option('--verb', '-v', default='post', help="The type of request to perform")
@click.option('--runasync', '-a', default=False, help="Run the requests asynchronously or not.")
@coro
async def get_average_response_time(runs: str, url: str, data: str, verb: str, runasync: bool) -> None:
    log_start(url, verb, runs)
    data = load_payload(data)

    print('Starting requests...async={}'.format(runasync))
    RequestService.runner(runasync, url, data, runs, verb)

    log_report(runs, RequestService.runtimes)


def load_payload(file_path: str) -> dict:
    with open(file_path) as f:
        print('\nLoading payload file: {}'.format(file_path))
        try:
            data = json.loads(f.read())
            print('Succesfully loaded payload file.\n')
            return data
        except Exception as error:
            print('Ran into error loading payload...exiting', error)
            raise error


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    get_average_response_time()
