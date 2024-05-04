"""create table kudo

Revision ID: 5ebdf2447502
Revises:
Create Date: 2024-04-26 16:41:20.555468

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5ebdf2447502'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    create table printers(
      id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
      ptype text,
      descrition text
    );
    """)


def downgrade() -> None:
    op.execute("""
    drop table if exists printers;
    """)
