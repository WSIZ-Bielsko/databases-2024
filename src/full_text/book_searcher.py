from asyncio import run
from uuid import UUID

from loguru import logger

from src.full_text.bookrepo import BookLineRepository
from src.full_text.common import connect_db


async def main():
    pool = await connect_db()
    repo = BookLineRepository(pool)

    logger.info('Full test search:')
    lines = await repo.search_ts_containing(
        book_id=UUID('9434ff35-e94b-49c8-b16f-811c09901935'), words=['Romeo', 'Juliet'])
    print(lines)

    logger.info('Similarity search')
    lines = await repo.search_body_similar(UUID('9434ff35-e94b-49c8-b16f-811c09901935'),
                                           line='sword')
    for ln in lines:
        print(ln)


if __name__ == '__main__':
    run(main())
