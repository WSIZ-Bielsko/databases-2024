"""create table users

Revision ID: 0441ee0be7a4
Revises: eee97d42e9e9
Create Date: 2024-05-11 13:12:31.141295

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0441ee0be7a4'
down_revision: Union[str, None] = 'eee97d42e9e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('create table users(id text primary key, name text not null)')


def downgrade() -> None:
    op.execute('drop table if exists users')
