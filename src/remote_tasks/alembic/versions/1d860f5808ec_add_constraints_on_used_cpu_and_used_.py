"""add constraints on used_cpu and used_ram on node

Revision ID: 1d860f5808ec
Revises: a594020ebb3d
Create Date: 2024-06-21 22:21:50.717006

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d860f5808ec'
down_revision: Union[str, None] = 'a594020ebb3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    ALTER TABLE node
    ADD CONSTRAINT check_used_cpu
    CHECK (used_cpu >= 0 AND used_cpu <= max_cpu);

    ALTER TABLE node
    ADD CONSTRAINT check_used_ram
    CHECK (used_ram >= 0 AND used_ram <= max_ram);
    
    """)


def downgrade() -> None:
    op.execute("""
    ALTER TABLE node DROP CONSTRAINT check_used_cpu;
    ALTER TABLE node DROP CONSTRAINT check_used_ram;
    """)
