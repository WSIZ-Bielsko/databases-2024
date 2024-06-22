"""add constraint job.unique_request_id

Revision ID: 58f5613f55de
Revises: 7217f0ebc09e
Create Date: 2024-06-21 17:21:12.696777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58f5613f55de'
down_revision: Union[str, None] = '7217f0ebc09e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    alter table job
    add constraint unique_request_id unique (request_id);
    """)


def downgrade() -> None:
    op.execute("""
    alter table job drop constraint unique_request_id;
    """)
