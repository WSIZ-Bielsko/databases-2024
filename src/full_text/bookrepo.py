from uuid import UUID

import asyncpg
from loguru import logger

from src.full_text.model import BookLine, SimilarityResult


class BookLineRepository:
    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    async def create(self, book_line: BookLine) -> BookLine:
        async with self.pool.acquire() as conn:
            query = """
                INSERT INTO booklines (line_number, book_id, body)
                VALUES ($1, $2, $3)
                RETURNING line_number, book_id, body
            """
            values = (book_line.line_number, book_line.book_id, book_line.body)
            row = await conn.fetchrow(query, *values)
            return BookLine(**row)

    async def read(self, line_number: int, book_id: UUID) -> BookLine | None:
        async with self.pool.acquire() as conn:
            query = """
                SELECT *
                FROM booklines
                WHERE line_number = $1 AND book_id = $2
            """
            values = (line_number, book_id)
            row = await conn.fetchrow(query, *values)
            return BookLine(**row) if row else None

    async def update(self, book_line: BookLine) -> BookLine:
        async with self.pool.acquire() as conn:
            query = """
                UPDATE booklines
                SET body = $3
                WHERE line_number = $1 AND book_id = $2
                RETURNING line_number, book_id, body
            """
            values = (book_line.line_number, book_line.book_id, book_line.body)
            row = await conn.fetchrow(query, *values)
            return BookLine(**row) if row else None

    async def delete(self, line_number: int, book_id: UUID) -> bool:
        async with self.pool.acquire() as conn:
            query = """
                DELETE FROM booklines
                WHERE line_number = $1 AND book_id = $2
            """
            values = (line_number, book_id)
            result = await conn.execute(query, *values)
            return result == "DELETE 1"

    # --------------

    async def search_primitive_containing(self, book_id: UUID, words: list[str]) -> list[BookLine]:
        async with self.pool.acquire() as conn:
            linked_words = ' || '.join(words)
            logger.warning(f'`{linked_words}`')
            # todo: won't work if >1 words present....
            records = await conn.fetch(
                """SELECT * FROM booklines
                   WHERE body LIKE '%' || $1 || '%'""",
                linked_words,
            )
            return [BookLine(**r) for r in records]

    async def search_ts_containing(self, book_id: UUID, words: list[str]) -> list[BookLine]:
        """
        Searches all booklines on the database for lines which contain
        _all_ the words present in `words` (allowing slight modifications of these),
        in any order.
        :param book_id:
        :param words:
        :return:
        """
        async with self.pool.acquire() as conn:
            query = """
            SELECT *
            FROM booklines
            WHERE to_tsvector('english', body) @@ to_tsquery($1);
            """
            linked_words = ' & '.join(words)
            logger.warning(f'`{linked_words}`')

            records = await conn.fetch(query, linked_words,)
            return [BookLine(**r) for r in records]

    async def search_body_similar(self, book_id: UUID, line: str) -> list[SimilarityResult]:
        """
        Finds all booklines which are similar to `line`.
        :param book_id:
        :param line:
        :return:
        """
        async with self.pool.acquire() as conn:
            query = """
            select *, similarity(body, $1) as sim from booklines where body % $1 order by sim desc;
            """
            records = await conn.fetch(query, line)
            return [SimilarityResult(bookline=BookLine(**r), similarity=r['sim']) for r in records]


    async def search_city_similar(self, city: str) -> list[dict]:
        """
        Finds all booklines which are similar to `line`.
        :param book_id:
        :param line:
        :return:
        """
        async with self.pool.acquire() as conn:
            query = """
            select *, similarity(city_ascii, $1) as sim from cities where city_ascii % $1 order by sim desc;
            """
            records = await conn.fetch(query, city)
            return [r for r in records]



    async def create_multiple(self, book_lines: list[BookLine]):
        query = '''
                INSERT INTO booklines (line_number, book_id, body)
                VALUES ($1, $2, $3)
            '''

        data = [(k.line_number, k.book_id, k.body) for k in book_lines]
        async with self.pool.acquire() as conn:
            await conn.executemany(query, data)
            await conn.close()
