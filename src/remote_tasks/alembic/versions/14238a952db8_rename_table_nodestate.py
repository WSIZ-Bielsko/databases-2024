"""rename table nodestate

Revision ID: 14238a952db8
Revises: 85b5052ca57a
Create Date: 2024-06-07 15:05:00.380330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14238a952db8'
down_revision: Union[str, None] = '85b5052ca57a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    alter table nodestate
    rename to node_state;
    ''')


def downgrade() -> None:
    op.execute('''
    alter table node_state
    rename to nodestate;
    ''')
