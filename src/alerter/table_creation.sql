

/*
write sql to create tables for the following pydantic data classes;

- use proper foreign keys with on delete cascade;
- name tables in plural;
- str should correspond to `text` fields


class Schedule(BaseModel):
    id: UUID
    name: str
    severity: int  # 0: weak, ... 2: medium... 5: critical
    period_days: int  # 0: will not be repeated
    next_alert_date: date | None


class Alert(BaseModel):
    id: UUID
    schedule_id: UUID
    message: str
    severity: int
    alert_date: date
    critical_warning_days_before: int
    closed_at: date


 */

 CREATE TABLE schedules (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    severity INTEGER NOT NULL,
    period_days INTEGER NOT NULL,
    next_alert_date DATE
);

-- Create alerts table
CREATE TABLE alerts (
    id UUID PRIMARY KEY,
    schedule_id UUID NOT NULL,
    message TEXT NOT NULL,
    severity INTEGER NOT NULL,
    alert_date DATE NOT NULL,
    critical_warning_days_before INTEGER NOT NULL,
    closed_at DATE,
    FOREIGN KEY (schedule_id) REFERENCES schedules(id) ON DELETE CASCADE
);