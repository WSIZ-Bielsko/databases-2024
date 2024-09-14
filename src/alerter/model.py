from datetime import date
from uuid import UUID

from pydantic import BaseModel


class Schedule(BaseModel):
    id: UUID
    active: bool = True
    name: str  # unique on DB
    description: str = ''
    severity: int = 5  # in [0..10]  --> 0: weak, ... 2: medium... 10: critical
    period_days: int | None  # 0: will not be repeated
    cron_expression: str | None = None
    critical_warning_days_before: int = 7


class Alert(BaseModel):
    id: UUID
    schedule_id: UUID
    message: str
    alert_date: date

    closed_at: date | None
    close_message: str | None


"""
Story: 
- scheduls are created by users: 
    - what, 
    - how often, 
    - how important
    
- an engine scans all schedules every 4h or so... to check if next alerts are created for them
    - if not -- creates an alert entity
    - if they exist, but have been closed -- creates an alert entity
    
- an engine scans all alerts periodically, and if an alert is upcoming, and closer than `days_before` 
    - creates a notification 
    - console, log, discord webhook (should be property of schedule in larger system)

"""
