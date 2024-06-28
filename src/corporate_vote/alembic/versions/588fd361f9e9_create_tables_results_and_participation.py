"""create tables results and participation

Revision ID: 588fd361f9e9
Revises: c357b3752b03
Create Date: 2024-06-28 12:22:21.158146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '588fd361f9e9'
down_revision: Union[str, None] = 'c357b3752b03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    -- Create the Results table
    CREATE TABLE results (
        vote_id SERIAL PRIMARY KEY,
        yes_count INTEGER NOT NULL DEFAULT 0,
        no_count INTEGER NOT NULL DEFAULT 0,
        pass_count INTEGER NOT NULL DEFAULT 0
    );

    -- Create the Participation table
    CREATE TABLE participation (
        vote_id INT references results(vote_id),
        email text references users(email),
        primary key (vote_id, email)
    );
    
    ''')


def downgrade() -> None:
    op.execute("""
    drop table if exists participation;
    drop table if exists results;
    """)
