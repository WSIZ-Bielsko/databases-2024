from uuid import UUID

import asyncpg

from src.full_text.model import BookLine


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

    async def search_primitive_containing(self, book_id: UUID, words: list[str]):
        pass

    async def search_ts_containing(self, book_id: UUID, words: list[str]):
        pass

    async def create_multiple(self, book_lines: list[BookLine]):
        query = '''
                INSERT INTO booklines (line_number, book_id, body)
                VALUES ($1, $2, $3)
            '''

        data = [(k.line_number, k.book_id, k.body) for k in book_lines]
        async with self.pool.acquire() as conn:
            await conn.executemany(query, data)
            await conn.close()


