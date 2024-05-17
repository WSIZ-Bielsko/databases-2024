from asyncio import run
from uuid import uuid4, UUID

from src.full_text.bookrepo import BookLineRepository
from src.full_text.common import connect_db
from src.full_text.model import BookLine

# Books from: https://www.gutenberg.org/browse/scores/top

def read_book(file_name: str, book_id: UUID | None = None) -> list[BookLine]:
    if not book_id:
        book_id = uuid4()
    with open(file_name, 'r') as f:
        lines = f.readlines()
        book_lines = [BookLine(line_number=i, book_id=book_id,  body=b)
                      for i, b in enumerate(lines)]
        return book_lines


async def main():
    pool = await connect_db()
    repo = BookLineRepository(pool)
    # line = BookLine(line_number=12, book_id=uuid4(),
    #                 body='Lorem ipsum dolor sit amet consectetur adipiscing elit')
    # x = await repo.create(line)
    # print(x)
    # lines = read_book('books/frankenstein.txt')
    lines = read_book('books/odyssey_homer.txt')

    await repo.create_multiple(lines)

    # for i, ln in enumerate(lines):
    #     if i%1000 == 0:
    #         print(f'done {i} of {len(lines)}')
    #     await repo.create(ln)


if __name__ == '__main__':
    run(main())
