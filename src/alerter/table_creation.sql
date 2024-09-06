

/*
write sql to create tables for the following pydantic data classes;

- use proper foreign keys with on delete cascade;
- name tables in plural;
- str should correspond to `text` fields
- create appropriate foreign keys with cascade delete


class Schedule(BaseModel):
    id: UUID
    active: bool = True
    name: str  # unique on DB
    description: str = ''
    severity: int = 5  # in [0..10]  --> 0: weak, ... 2: medium... 10: critical
    period_days: int  # 0: will not be repeated
    critical_warning_days_before: int = 7


class Alert(BaseModel):
    id: UUID
    schedule_id: UUID
    message: str
    alert_date: date

    closed_at: date | None
    close_message: str | None

 */

 -- Create Schedules table
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