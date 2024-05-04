"""add column printed_pages to printers

Revision ID: 6445ee0eb703
Revises: 5ebdf2447502
Create Date: 2024-04-26 17:02:31.382902

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6445ee0eb703'
down_revision: Union[str, None] = '5ebdf2447502'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    alter table printers add column printed_pages int default 0;
    """)


def downgrade() -> None:
    op.execute("""
    alter table printers drop column printed_pages;
    """)
