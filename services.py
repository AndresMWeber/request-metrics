import json
import time
from timeit import default_timer as timer
import sys
import asyncio
import aiohttp
import requests
from utils import log_end_response, log_report, config, coro


class RequestService:
    runtimes = []

    @classmethod
    @coro
    async def runner(cls, runAsync, url: str, data: dict, runs: int, verb: str):
        request_args = cls.create_payload(url, data)

        if runAsync:
            await cls.do_requests(url, request_args, runs, verb)
        else:
            cls.do_requests_sync(url, request_args, runs, verb)

    @classmethod
    async def do_requests(cls, url: str, request_args: dict, runs: int, verb: str):
        cls.runtimes = []
        tasks = []
        async with aiohttp.ClientSession() as session:
            for _ in range(runs):
                task = cls.do_request(session, url, request_args, runs, verb)
                tasks.append(task)
            _ = await asyncio.gather(*tasks)

    @classmethod
    async def do_request(cls, session: aiohttp.ClientSession, url: str, request_args: dict, runs: int, verb: str) -> None:
        start_time = timer()
        async with getattr(session, verb)(**request_args) as response:
            elapsed = float(timer() - start_time)
            if response.status == 200:
                cls.runtimes.append(elapsed)
            log_end_response(response.status, elapsed)

    @classmethod
    def do_requests_sync(cls, url: str, request_args: dict, runs: int, verb: str):
        cls.runtimes = []
        for _ in range(runs):
            cls.do_request_sync(url, request_args, runs, verb)

    @classmethod
    def do_request_sync(cls, url: str, request_args: dict, runs: int, verb: str) -> None:
        response = getattr(requests, verb)(**request_args)
        if response.status_code == 200:
            cls.runtimes.append(response.elapsed.total_seconds())
        log_end_response(response.status_code, response.elapsed.total_seconds())

    @staticmethod
    def create_payload(url, data):
        payload = {"url": url}
        if data:
            payload.update(
                {"headers": config.JSON_HEADER, "data": json.dumps(data)})
        return payload
