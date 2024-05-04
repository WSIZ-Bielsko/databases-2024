"""create table kudo

Revision ID: eee97d42e9e9
Revises: 6445ee0eb703
Create Date: 2024-04-26 23:36:57.203849

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'eee97d42e9e9'
down_revision: Union[str, None] = '6445ee0eb703'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    create table Kudo
(
    id       UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    purpose  TEXT,
    owner_id TEXT NOT NULL
);
    """)


def downgrade() -> None:
    op.execute("""
    drop table if exists Kudo;
    """)
