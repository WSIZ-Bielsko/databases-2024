"""add cancelled_at for tasks

Revision ID: 2ba3b960f86e
Revises: 50619dff3cad
Create Date: 2024-06-11 19:35:54.454837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '2ba3b960f86e'
down_revision: Union[str, None] = '50619dff3cad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    ALTER TABLE JobRequest
    ADD COLUMN cancelled_at TIMESTAMP;
    """)


def downgrade() -> None:
    op.execute("""
    ALTER TABLE JobRequest
DROP COLUMN cancelled_at;
    """)
