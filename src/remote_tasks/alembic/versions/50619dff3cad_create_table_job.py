"""create table job

Revision ID: 50619dff3cad
Revises: 14238a952db8
Create Date: 2024-06-10 12:30:32.795020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50619dff3cad'
down_revision: Union[str, None] = '14238a952db8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE job (
    id UUID PRIMARY KEY,
    request_id UUID REFERENCES JobRequest(id) ON DELETE CASCADE,
    node_id UUID REFERENCES Node(id) ON DELETE CASCADE,
    started_at TIMESTAMP NOT NULL,
    canceled_at TIMESTAMP NULL,
    finished_at TIMESTAMP NULL
);
    """)


def downgrade() -> None:
    op.execute("""
    drop table if exists job;
    """)