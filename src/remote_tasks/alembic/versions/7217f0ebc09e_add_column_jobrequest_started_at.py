"""add column jobrequest.started_at

Revision ID: 7217f0ebc09e
Revises: bd7fb731e6e6
Create Date: 2024-06-13 11:20:13.794041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7217f0ebc09e'
down_revision: Union[str, None] = 'bd7fb731e6e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    alter table jobrequest add column started_at timestamp;
    """)


def downgrade() -> None:
    op.execute("""
    alter table jobrequest drop column started_at;
    """)
