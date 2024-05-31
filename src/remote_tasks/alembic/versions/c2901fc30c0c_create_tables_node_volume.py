"""create tables node, volume

Revision ID: c2901fc30c0c
Revises: aedc18e699d8
Create Date: 2024-05-31 17:21:05.274659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2901fc30c0c'
down_revision: Union[str, None] = 'aedc18e699d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE Node (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    max_cpu FLOAT NOT NULL,
    max_ram FLOAT NOT NULL
);

CREATE TABLE Volume (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL
);

    
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE node;
    DROP TABLE volume;
    
    """)
