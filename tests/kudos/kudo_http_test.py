from uuid import uuid4

import pytest
from aiohttp.test_utils import TestClient
from http_conftest import cli
from src.kudos.kudo_repository import KudoRepository
from src.kudos.model import Kudo


@pytest.mark.asyncio
async def test_healthy(cli: TestClient):
    resp = await cli.get('/status')

    assert resp.status == 200
    assert (await resp.json()).get('status') == 'ok'


@pytest.mark.asyncio
async def test_get_kudo(cli: TestClient, kudo1: Kudo):
    kudo_id = kudo1.id
    resp = await cli.get(f'kudos/{kudo_id}')

    assert resp.status == 200
    kudo_resp = Kudo(**(await resp.json()))
    assert kudo_resp == kudo1


@pytest.mark.asyncio
async def test_create_kudo(cli: TestClient, kudoRepo: KudoRepository):
    kudo = Kudo(id=uuid4(), purpose='http_creation', owner_id='s11')
    resp = await cli.post(f'kudos', json=kudo.model_dump())
    kudo_in_db = await kudoRepo.read(kudo.id)

    assert resp.status == 200
    kudo_resp = Kudo(**(await resp.json()))
    assert kudo == kudo_resp
    assert kudo == kudo_in_db

    await kudoRepo.delete(kudo.id)


@pytest.mark.asyncio
async def test_update_kudo(cli: TestClient, kudo1: Kudo, kudoRepo: KudoRepository):
    kudo1.purpose = 'changed_purpose'
    resp = await cli.put(f'kudos/{kudo1.id}', json=kudo1.model_dump())
    kudo_in_db = await kudoRepo.read(kudo1.id)

    assert resp.status == 204
    assert kudo_in_db.purpose == kudo1.purpose


@pytest.mark.asyncio
async def test_delete_kudo(cli: TestClient, kudo1: Kudo, kudoRepo: KudoRepository):
    resp = await cli.delete(f'kudos/{kudo1.id}')
    kudo_in_db = await kudoRepo.read(kudo1.id)

    assert resp.status == 204
    assert kudo_in_db is None
