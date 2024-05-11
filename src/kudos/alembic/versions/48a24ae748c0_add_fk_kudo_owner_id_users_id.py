"""add FK kudo.owner_id -> users.id

Revision ID: 48a24ae748c0
Revises: 0441ee0be7a4
Create Date: 2024-05-11 13:18:35.252639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48a24ae748c0'
down_revision: Union[str, None] = '0441ee0be7a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    alter table kudo
    add constraint kudo_users_id_fk
        foreign key (owner_id) references users
            on delete cascade;
    """)


def downgrade() -> None:
    op.execute("""
    alter table kudo drop constraint kudo_users_id_fk
    """)
