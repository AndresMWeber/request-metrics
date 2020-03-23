#!/usr/bin/env python
import click
import json
from services import RequestService
from utils import log_start, log_end_response, log_report, config, coro, Notifier


@click.command()
@click.option('--runs', '-r', default=10, help="Number of requests to run.")
@click.option('--url', '-u', default=config.ENDPOINT, help="API Endpoint to post to.")
@click.option('--data', '-d', default=config.PAYLOAD_FILE, help="Allows adding body data via a string or specified JSON file (default is payload_data.json) (if using POST).")
@click.option('--headers', '-h', default=config.PAYLOAD_FILE, help="Allows adding headers via a string or specified JSON file (default is payload_headers.json).")
@click.option('--action', '-a', default='post', help="The type of request to perform")
@click.option('--runasync', '-c', default=False, help="Run the requests asynchronously or not.")
@click.option('--verbose', '-v', default=False, help="Verbose mode.")
def get_average_response_time(url: str, action: str, data: str, headers: str, runs: str, verbose: bool, runasync: bool) -> None:
    Notifier.verbose = verbose
    log_start(url, action, runs)

    Notifier.emit('Loading payload data')
    data = load_payload(data)

    Notifier.emit('Loading payload headers')
    headers = load_payload(headers)

    Notifier.emit('\nRunning requests {}:'.format('asynchronously' if runasync else 'synchronously'))
    RequestService.runner(runasync, url, data, runs, action, headers)

    log_report(runs, RequestService.runtimes)


def load_payload(file_path: str) -> dict:
    data = None
    try:
        Notifier.emit('\tPayload is string formatted JSON...', end='')
        data = json.loads(file_path)
        Notifier.emit('true.')
        return data
    except json.decoder.JSONDecodeError as error:
        Notifier.emit('false: "{}"'.format(error))
    
    with open(file_path) as f:
        Notifier.emit('\tPayload is a JSON file "{}"...'.format(file_path), end='')
        try:
            data = json.loads(f.read())
            Notifier.emit('true.')
            return data
        except Exception as error:
            Notifier.emit('false: "{}"'.format(error))
            raise error


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    get_average_response_time()
