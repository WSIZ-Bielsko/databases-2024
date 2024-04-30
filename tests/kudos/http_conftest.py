import pytest_asyncio

from src.kudos.kudos_app import app_factory


@pytest_asyncio.fixture
async def app_fixture():
    return await app_factory()


@pytest_asyncio.fixture
async def cli(aiohttp_client, app_fixture):
    return await aiohttp_client(app_fixture)