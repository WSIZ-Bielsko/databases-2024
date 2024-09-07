"""create tables schedules and alerts

Revision ID: bcdd6bb7ad4a
Revises: 
Create Date: 2024-09-06 17:17:17.390964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcdd6bb7ad4a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
CREATE TABLE schedules (
    id UUID PRIMARY KEY,
    active BOOLEAN DEFAULT TRUE,
    name TEXT UNIQUE NOT NULL,
    description TEXT DEFAULT '',
    severity INTEGER DEFAULT 5 CHECK (severity >= 0 AND severity <= 10),
    period_days INTEGER NOT NULL,
    critical_warning_days_before INTEGER DEFAULT 7
);

-- Create alerts table
CREATE TABLE alerts (
    id UUID PRIMARY KEY,
    schedule_id UUID NOT NULL,
    message TEXT NOT NULL,
    alert_date DATE NOT NULL,
    closed_at DATE,
    close_message TEXT,
    FOREIGN KEY (schedule_id) REFERENCES schedules(id) ON DELETE CASCADE
);    
    
    
    """)


def downgrade() -> None:
    op.execute("""
        DROP TABLE IF EXISTS schedules, alerts; 
    """)
