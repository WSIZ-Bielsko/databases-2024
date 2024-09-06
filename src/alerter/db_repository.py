

"""
Write a class EntityRepository with methods for CRUD operations using asyncpg
for the following pydantic data classes:


class Schedule(BaseModel):
    id: UUID
    name: str
    severity: int  # 0: weak, ... 2: medium... 5: critical
    period_days: int  # 0: will not be repeated
    next_alert_date: date | None
    action: str # 'log' or 'discord'


class Alert(BaseModel):
    id: UUID
    schedule_id: UUID
    message: str
    severity: int
    alert_date: date
    critical_warning_days_before: int
    closed_at: date

Apart from the method corresponding to delete operation, all other ms should return
instance or instances of the dataclass or None.

Assume connection pool is assigned in constructor of EntityRepository.

In the result, replace "Optional" by " | None" python construct.

Create instances of the dataclass by (**result) code.

Use `select *` in list and get methods.

Use modern python syntax (python >= 3.11), don't use the typing package.

In update method use "returning *" in sql.

Use plural for table name in sql.

The methods should have a suffix equal to the dataclass name.

"""
from uuid import UUID

import asyncpg

from src.alerter.model import Schedule, Alert


class EntityRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def create_schedule(self, schedule: Schedule) -> Schedule | None:
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow(
                """
                INSERT INTO schedules (id, name, severity, period_days, next_alert_date, action)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING *
                """,
                schedule.id, schedule.name, schedule.severity, schedule.period_days,
                schedule.next_alert_date, schedule.action
            )
            return Schedule(**result) if result else None

    async def get_schedule(self, schedule_id: UUID) -> Schedule | None:
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow("SELECT * FROM schedules WHERE id = $1", schedule_id)
            return Schedule(**result) if result else None

    async def list_schedules(self) -> list[Schedule]:
        async with self.pool.acquire() as conn:
            results = await conn.fetch("SELECT * FROM schedules")
            return [Schedule(**result) for result in results]

    async def update_schedule(self, schedule: Schedule) -> Schedule | None:
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow(
                """
                UPDATE schedules
                SET name = $2, severity = $3, period_days = $4, next_alert_date = $5, action = $6
                WHERE id = $1
                RETURNING *
                """,
                schedule.id, schedule.name, schedule.severity, schedule.period_days,
                schedule.next_alert_date, schedule.action
            )
            return Schedule(**result) if result else None

    async def delete_schedule(self, schedule_id: UUID) -> None:
        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM schedules WHERE id = $1", schedule_id)

    async def create_alert(self, alert: Alert) -> Alert | None:
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow(
                """
                INSERT INTO alerts (id, schedule_id, message, severity, alert_date, critical_warning_days_before, closed_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING *
                """,
                alert.id, alert.schedule_id, alert.message, alert.severity,
                alert.alert_date, alert.critical_warning_days_before, alert.closed_at
            )
            return Alert(**result) if result else None

    async def get_alert(self, alert_id: UUID) -> Alert | None:
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow("SELECT * FROM alerts WHERE id = $1", alert_id)
            return Alert(**result) if result else None

    async def list_alerts(self) -> list[Alert]:
        async with self.pool.acquire() as conn:
            results = await conn.fetch("SELECT * FROM alerts")
            return [Alert(**result) for result in results]

    async def update_alert(self, alert: Alert) -> Alert | None:
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow(
                """
                UPDATE alerts
                SET schedule_id = $2, message = $3, severity = $4, alert_date = $5, critical_warning_days_before = $6, closed_at = $7
                WHERE id = $1
                RETURNING *
                """,
                alert.id, alert.schedule_id, alert.message, alert.severity,
                alert.alert_date, alert.critical_warning_days_before, alert.closed_at
            )
            return Alert(**result) if result else None

    async def delete_alert(self, alert_id: UUID) -> None:
        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM alerts WHERE id = $1", alert_id)