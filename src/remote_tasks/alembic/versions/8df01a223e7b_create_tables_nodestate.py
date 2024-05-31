"""create tables nodestate

Revision ID: 8df01a223e7b
Revises: c2901fc30c0c
Create Date: 2024-05-31 17:25:37.775426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8df01a223e7b'
down_revision: Union[str, None] = 'c2901fc30c0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE NodeState (
    id UUID PRIMARY KEY,
    node_id UUID NOT NULL,
    reported_at TIMESTAMP NOT NULL,
    used_cpu FLOAT NOT NULL,
    used_ram FLOAT NOT NULL,
    FOREIGN KEY (node_id) REFERENCES Node(id) ON DELETE CASCADE
);
    
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE nodestate;
    """)
