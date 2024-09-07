

"""
Write a class EntityRepository with methods for CRUD operations using asyncpg
for the following pydantic data classes:


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
import asyncio
import os
from asyncio import run
from datetime import date, timedelta
from uuid import UUID, uuid4

import asyncpg
from asyncpg import Pool
from dotenv import load_dotenv
from loguru import logger

from src.alerter.model import Schedule, Alert


async def connect_db() -> Pool:
    load_dotenv()
    logger.info("Loading env variables")
    url = os.getenv("DB_URL", None)

    pool = await asyncpg.create_pool(
        url, min_size=5, max_size=10, timeout=30, command_timeout=5
    )
    return pool


class EntityRepository:
    def __init__(self, pool):
        self.pool = pool

    async def create_schedule(self, schedule: Schedule) -> Schedule | None:
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow(
                """
                INSERT INTO schedules (id, active, name, description, severity, period_days, critical_warning_days_before)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING *
                """,
                schedule.id, schedule.active, schedule.name, schedule.description,
                schedule.severity, schedule.period_days, schedule.critical_warning_days_before
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
                SET active = $2, name = $3, description = $4, severity = $5, period_days = $6, critical_warning_days_before = $7
                WHERE id = $1
                RETURNING *
                """,
                schedule.id, schedule.active, schedule.name, schedule.description,
                schedule.severity, schedule.period_days, schedule.critical_warning_days_before
            )
            return Schedule(**result) if result else None

    async def delete_schedule(self, schedule_id: UUID) -> None:
        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM schedules WHERE id = $1", schedule_id)

    async def create_alert(self, alert: Alert) -> Alert | None:
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow(
                """
                INSERT INTO alerts (id, schedule_id, message, alert_date, closed_at, close_message)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING *
                """,
                alert.id, alert.schedule_id, alert.message, alert.alert_date,
                alert.closed_at, alert.close_message
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
                SET schedule_id = $2, message = $3, alert_date = $4, closed_at = $5, close_message = $6
                WHERE id = $1
                RETURNING *
                """,
                alert.id, alert.schedule_id, alert.message, alert.alert_date,
                alert.closed_at, alert.close_message
            )
            return Alert(**result) if result else None

    async def delete_alert(self, alert_id: UUID) -> None:
        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM alerts WHERE id = $1", alert_id)

    # ------------------ custom methods -----------------

    async def get_last_alert(self, schedule_id: UUID) -> Alert | None:
        pass




async def main():
    pool = await connect_db()
    db = EntityRepository(pool)
    s = Schedule(id=uuid4(), name='podatek VAT do US', description='Works well when paid on time', period_days=30)
    logger.info(f'saving {s} to db')
    await db.create_schedule(s)
    logger.info('schedule saved')
    a = Alert(id=uuid4(), schedule_id=s.id, message="podatek do zapłaty",
              alert_date=date.today() + timedelta(days=s.period_days), closed_at=None, close_message=None)
    await db.create_alert(a)



if __name__ == '__main__':
    run(main())