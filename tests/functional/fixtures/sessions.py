import asyncio
import aiohttp
import pytest


async def get_aiohttp_client() -> aiohttp.ClientSession:
    """
    Returns client inside async function. Done to prevent warnings.

    Returns:
         Aiohttp client session
    """
    return aiohttp.ClientSession()


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def aiohttp_client(event_loop: asyncio.AbstractEventLoop):
    client = event_loop.run_until_complete(get_aiohttp_client())
    yield client
    event_loop.run_until_complete(client.close())
