import asyncio
import os

import snug
from dotenv import load_dotenv

from electron import (
    async_executor,
    electricity_maps,
    execute,
    execute_async,
    executor,
    token_auth,
)


def main():
    q = electricity_maps.power_breakdown.get_history("BE")
    # assert reveal_type(q) = Query[PowerBreakdownHistory]

    r = execute(q, auth=token_auth(API_TOKEN))
    # assert reveal_type(r) = PowerBreakdownHistory

    # in theory should be the same with snug.execute
    # but for now only works on tooltip as it uses docstring type info
    _r = snug.execute(q, auth=token_auth(API_TOKEN))
    # assert reveal_type(_r) = PowerBreakdownHistory

    client = executor(auth=token_auth(API_TOKEN))
    rr = client(q)
    # assert reveal_type(rr) = PowerBreakdownHistory

    # in theory should be the same with snug.executor
    # but for now only works on tooltip as it uses docstring type info
    _client = snug.executor(auth=token_auth(API_TOKEN))
    _rr = _client(q)
    # assert reveal_type(_rr) = PowerBreakdownHistory

    return r.zone, rr.zone


async def main_async():
    q = electricity_maps.power_breakdown.get_history("BE")
    # assert reveal_type(q) = Query[PowerBreakdownHistory]

    r = await execute_async(q, auth=token_auth(API_TOKEN))
    # assert reveal_type(r) = PowerBreakdownHistory

    # in theory should be the same with snug.execute_async
    # but for now doesn't even work at all (tooltip / mypy)
    # _r = snug.execute_async(q, auth=token_auth(API_TOKEN))
    # assert reveal_type(_r) = PowerBreakdownHistory

    client = async_executor(auth=token_auth(API_TOKEN))
    rr = await client(q)
    # assert reveal_type(rr) = PowerBreakdownHistory

    # in theory should be the same with snug.async_executor
    # but for now doesn't even work at all (tooltip / mypy)
    # _client = snug.async_executor(auth=token_auth(API_TOKEN))
    # _rr = await _client(q)
    # assert reveal_type(_rr) = PowerBreakdownHistory

    return r.zone, rr.zone


if __name__ == "__main__":
    load_dotenv()
    API_TOKEN = os.environ.get("API_TOKEN")

    out = main()
    print(out)

    coro = main_async()
    out = asyncio.run(coro)
    print(out)
