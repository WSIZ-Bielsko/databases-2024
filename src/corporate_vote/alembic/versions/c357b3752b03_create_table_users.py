"""create table users

Revision ID: c357b3752b03
Revises: 
Create Date: 2024-06-28 12:00:24.916655

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c357b3752b03'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table users (
        id UUID PRIMARY KEY,
        email text NOT NULL UNIQUE,
        password text NOT NULL,
        token text,
        shares INTEGER DEFAULT 0,
        active BOOLEAN DEFAULT TRUE
    );
    ''')


def downgrade() -> None:
    op.execute('''
    drop table if exists users
    ''')
