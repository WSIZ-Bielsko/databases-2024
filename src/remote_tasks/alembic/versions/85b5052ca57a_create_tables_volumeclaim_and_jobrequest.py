"""create tables volumeclaim and jobrequest

Revision ID: 85b5052ca57a
Revises: 8df01a223e7b
Create Date: 2024-05-31 17:31:48.900389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85b5052ca57a'
down_revision: Union[str, None] = '8df01a223e7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    
CREATE TABLE JobRequest (
    id UUID PRIMARY KEY,
    repo_url TEXT NOT NULL,
    commit TEXT NOT NULL,
    image_tag TEXT NOT NULL,
    entry_point_file TEXT NOT NULL,
    env_file_content TEXT NOT NULL,
    cpu FLOAT NOT NULL,
    ram_mb FLOAT NOT NULL,
    priority INT NOT NULL,
    user_id UUID NOT NULL,
    submitted_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

    
    CREATE TABLE VolumeClaim (
    id UUID PRIMARY KEY,
    volume_id UUID NOT NULL,
    job_request_id UUID NOT NULL,
    mount_type TEXT NOT NULL,
    FOREIGN KEY (volume_id) REFERENCES Volume(id) ON DELETE CASCADE,
    FOREIGN KEY (job_request_id) REFERENCES JobRequest(id) ON DELETE CASCADE
);


    
    """)


def downgrade() -> None:
    op.execute("""
    drop table volumeclaim;
    drop table jobrequest;
    
    """)
