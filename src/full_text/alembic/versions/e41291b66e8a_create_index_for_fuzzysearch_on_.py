"""create index for fuzzysearch on booklines.body

Revision ID: e41291b66e8a
Revises: d4afad472174
Create Date: 2024-05-18 13:21:37.982084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e41291b66e8a'
down_revision: Union[str, None] = 'd4afad472174'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE INDEX trgm_idx ON booklines USING GIN (body gin_trgm_ops);
    """)


def downgrade() -> None:
    op.execute("""
    drop index trgm_idx;
    """)
