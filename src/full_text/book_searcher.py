import os
from asyncio import run
from uuid import UUID

from loguru import logger

from src.full_text.bookrepo import BookLineRepository
from src.full_text.common import connect_db


async def main():
    pool = await connect_db()
    repo = BookLineRepository(pool)

    while (True):

        logger.info('Full text search:')

        s = input('podaj szukane słowa>')
        words = s.strip().split(' ')
        if len(words) == 1 and words[0]=='':
            break

        # lines = await repo.search_ts_containing(
        #     book_id=UUID('9434ff35-e94b-49c8-b16f-811c09901935'), words=words)
        # print(lines)

        # logger.info('Similarity search')
        # lines = await repo.search_body_similar(UUID('9434ff35-e94b-49c8-b16f-811c09901935'),
        #                                        line=words[0])
        lines = await repo.search_city_similar(city=words[0])
        print('wynik wyszukiwania:')
        for ln in lines:
            print(ln)


if __name__ == '__main__':
    run(main())
