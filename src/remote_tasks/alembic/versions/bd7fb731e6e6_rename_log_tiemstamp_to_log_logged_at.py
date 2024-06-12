"""rename log.tiemstamp to log.logged_at

Revision ID: bd7fb731e6e6
Revises: 5e4afb738ed8
Create Date: 2024-06-12 11:34:48.648341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd7fb731e6e6'
down_revision: Union[str, None] = '5e4afb738ed8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    alter table log rename column timestamp to logged_at
    """)


def downgrade() -> None:
    op.execute("""
    alter table log rename column logged_at to timestamp
    """)
