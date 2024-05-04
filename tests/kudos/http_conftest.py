import pytest_asyncio

from src.kudos.kudos_app import app_factory


# @pytest_asyncio.fixture
# async def app_fixture():
#     return await app_factory()


@pytest_asyncio.fixture
async def cli(aiohttp_client):
    return await aiohttp_client(await app_factory())