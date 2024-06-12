"""create table log

Revision ID: 5e4afb738ed8
Revises: 2ba3b960f86e
Create Date: 2024-06-12 11:14:30.561300

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e4afb738ed8'
down_revision: Union[str, None] = '2ba3b960f86e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE Log (
    id UUID PRIMARY KEY,
    job_id UUID NOT NULL REFERENCES job(id) on delete cascade ,
    timestamp TIMESTAMP NOT NULL,
    stream TEXT CHECK (stream IN ('stdout', 'stderr')),
    level TEXT,
    message TEXT
);
""")


def downgrade() -> None:
    op.execute("""drop table if exists Log """)
