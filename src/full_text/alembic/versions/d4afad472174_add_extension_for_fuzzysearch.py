"""add extension for fuzzysearch

Revision ID: d4afad472174
Revises: a7a901f4d923
Create Date: 2024-05-18 13:19:40.904310

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4afad472174'
down_revision: Union[str, None] = 'a7a901f4d923'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE EXTENSION pg_trgm;
    """)


def downgrade() -> None:
    op.execute("""
    drop extension pg_trgm;
    """)
