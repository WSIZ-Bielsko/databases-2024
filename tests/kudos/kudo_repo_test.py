from uuid import uuid4

import pytest
from loguru import logger

from src.kudos.kudo_repository import KudoRepository
from src.kudos.model import Kudo


@pytest.mark.asyncio
async def test_db_healthy(kudoRepo: KudoRepository):
    await kudoRepo.get_kudos_by_personid(str(uuid4()))
    logger.info("ok")


@pytest.mark.asyncio
async def test_kudo1_exists(kudoRepo: KudoRepository, kudo1: Kudo):
    logger.info(f"checking if fixture kudo1 worked; id={kudo1.id}")
    prepared_kudo = await kudoRepo.read(kudo_id=kudo1.id)
    logger.info(f"fetched kudo={prepared_kudo}")
    assert prepared_kudo is not None


@pytest.mark.asyncio
async def test_can_update_kudo_purpose(kudoRepo: KudoRepository, kudo1: Kudo):
    kudo1.purpose = "update_test"
    await kudoRepo.update(kudo1)
    updated = await kudoRepo.read(kudo1.id)
    logger.debug(f"updated kudo1: {updated}")
    assert updated.purpose == "update_test"


@pytest.mark.asyncio
async def test_fetch_multiple_kudos(kudoRepo: KudoRepository, kudo1: Kudo, kudo2: Kudo):
    all_kudos_of_person = await kudoRepo.get_kudos_by_personid(kudo1.owner_id)
    logger.debug(f"all kudos of owner {kudo1.owner_id}: {all_kudos_of_person}")
    assert len(all_kudos_of_person) == 2


@pytest.mark.asyncio
async def test_can_have_two_kudos_with_same_purpose(kudoRepo: KudoRepository, kudo1: Kudo):
    kudo_new = Kudo(id=uuid4(), purpose=kudo1.purpose, owner_id=kudo1.owner_id)

    await kudoRepo.create(kudo_new)

    saved = await kudoRepo.read(kudo_new.id)

    assert kudo_new == saved
