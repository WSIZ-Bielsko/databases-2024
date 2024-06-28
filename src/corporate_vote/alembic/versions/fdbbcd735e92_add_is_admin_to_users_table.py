"""add is_admin to users table

Revision ID: fdbbcd735e92
Revises: 588fd361f9e9
Create Date: 2024-06-28 13:55:01.585652

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fdbbcd735e92'
down_revision: Union[str, None] = '588fd361f9e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    alter table users add is_admin boolean default false;
    """)


def downgrade() -> None:
    op.execute("""alter table users drop is_admin;""")
