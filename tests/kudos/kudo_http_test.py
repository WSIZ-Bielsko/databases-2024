import pytest
from aiohttp.test_utils import TestClient
from http_conftest import cli, app_fixture


@pytest.mark.asyncio
async def test_healthy(cli: TestClient):
    resp = await cli.get('/status')

    assert resp.status == 200
    assert (await resp.json()).get('status') == 'ok'
