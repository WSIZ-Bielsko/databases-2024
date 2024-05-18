"""add index for full-text search

Revision ID: a7a901f4d923
Revises: cab3f5635a99
Create Date: 2024-05-17 18:52:40.384059

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7a901f4d923'
down_revision: Union[str, None] = 'cab3f5635a99'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE INDEX idx_books ON booklines USING GIN (to_tsvector('english', body));
    """)


def downgrade() -> None:
    op.execute("""
    DROP INDEX IF EXISTS idx_books;
    """)
