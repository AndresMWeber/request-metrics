#!/usr/bin/env python
import json
import time
from timeit import default_timer as timer
import sys
import click
import asyncio
import aiohttp
from utils import log_start, log_end_response, log_report, config, coro


@click.command()
@click.option('--runs', '-r', default=10, help="Number of requests to run.")
@click.option('--url', '-u', default=config.PASSES_ENDPOINT, help="API Endpoint to post to.")
@click.option('--data', '-d', default=config.PASS_PAYLOAD_FILE, help="JSON data (if using POST).")
@click.option('--verb', '-v', default='post', help="The type of request to perform")
@coro
async def get_average_response_time(runs: str, url: str, data: str, verb: str) -> None:
    log_start(url, verb, runs)

    tasks = []
    do_request.runtimes = []
    do_request.start_time = dict()
    data = load_payload(data)

    async with aiohttp.ClientSession() as session:
        print('Starting requests...')
        for _ in range(runs):
            task = asyncio.ensure_future(
                do_request(session, url, data, runs, verb))
            tasks.append(task)
        _ = await asyncio.gather(*tasks)

    log_report(runs, do_request.runtimes)


async def do_request(session: aiohttp.ClientSession, url: str, payload: dict, runs: int, verb: str) -> None:
    request_args = {"url": url}
    if payload:
        request_args.update(
            {"headers": config.JSON_HEADER, "data": json.dumps(payload)})

    start_time = timer()
    async with getattr(session, verb)(**request_args) as response:
        if response.status == 200:
            do_request.runtimes.append(timer() - start_time)
        response.elapsed = timer() - start_time
        log_end_response(response)


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
    loop = asyncio.get_event_loop()
    start_time = time.time()
    # pylint: disable=no-value-for-parameter
    task = loop.create_task(get_average_response_time())
    loop.run_until_complete(task)
    duration = time.time() - start_time
    print(f"Requests finished in {duration} seconds")
