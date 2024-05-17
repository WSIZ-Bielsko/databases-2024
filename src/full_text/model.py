from uuid import UUID

from pydantic import BaseModel


class BookLine(BaseModel):
    line_number: int
    book_id: UUID
    body: str


