"""create table booklines

Revision ID: cab3f5635a99
Revises: 
Create Date: 2024-05-17 16:52:16.108100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cab3f5635a99'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    create table booklines(
        line_number int,
        book_id UUID,
        body text,
        PRIMARY KEY (book_id, line_number)
    );
    """)


def downgrade() -> None:
    op.execute("""
    drop table if exists booklines;
    """)
