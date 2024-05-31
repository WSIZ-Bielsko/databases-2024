"""create table users

Revision ID: aedc18e699d8
Revises: 
Create Date: 2024-05-31 17:12:44.897088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aedc18e699d8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE users (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL
);
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE users
    
    """)
