"""add columns used_ram,used_cpu to node

Revision ID: a594020ebb3d
Revises: 58f5613f55de
Create Date: 2024-06-21 22:08:39.854075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a594020ebb3d'
down_revision: Union[str, None] = '58f5613f55de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        alter table node add column used_ram double precision default 0;
        alter table node add column used_cpu double precision default 0;    
    """)


def downgrade() -> None:
    op.execute("""
    alter table node drop column  used_cpu;
    alter table node drop column  used_ram;
    """)