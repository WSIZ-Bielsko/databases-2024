import asyncio
from asyncio import run
from uuid import uuid4, UUID

from asyncpg.pgproto.pgproto import timedelta
from dateutil.utils import today
from loguru import logger
from pydantic import BaseModel
from pydantic.v1 import UUID1

from src.alerter.db_repository import EntityRepository, connect_db
from src.alerter.model import Alert


class EngineConfig(BaseModel):
    check_schedule_hours: int = 1


class AlerterEngine:

    def __init__(self, db: EntityRepository, config: EngineConfig):
        self.config = config
        self.db = db

    async def run(self):
        logger.info('Starting alerter engine')

        while True:
            await self.schedule_alerts()
            await self.notify_on_alerts()
            next_action = self.config.check_schedule_hours * 3600
            logger.info(f'sleeping for {next_action / 3600} hours')
            await asyncio.sleep(self.config.check_schedule_hours * 3600)

    async def schedule_alerts(self):
        logger.info('Checking schedule for new alerts to create')

        schedules = await self.db.list_active_schedules()

        for s in schedules:
            last_alert = await self.db.get_last_alert(s.id)
            if last_alert is None:
                new_alert = Alert(id=uuid4(), schedule_id=s.id,
                                  message=f'new alert for schedule {s.name}',
                                  alert_date=today() + timedelta(days=s.period_days),
                                  closed_at=None,
                                  close_message=None)
                logger.info('creating new alert ' + str(new_alert))
                await self.db.create_alert(new_alert)

    async def notify_on_alerts(self):
        logger.info('Acting on alerts')
        alerts = await self.db.list_alerts()
        for a in alerts:
            schedule = await self.db.get_schedule(a.schedule_id)
            if (a.alert_date - today()).days <= schedule.critical_warning_days_before:
                logger.warning('ALERT DUE:' + a.message)

        # pull all non-closed alerts
        # if they are close to alert_date:
        #   if severity <= 5 --> write a "warning" log to console
        #   else --> send alert message to discord (for now implement as if this were to console with extra WARNING in message

    async def close_alert(self, alert_id: UUID, close_message: str):
        alert = await self.db.get_alert(alert_id)
        alert.closed_at = today()
        alert.close_message = close_message
        await self.db.update_alert(alert)


async def main():
    logger.info('Starting alerter engine')
    pool = await connect_db()
    db = EntityRepository(pool=pool)
    engine = AlerterEngine(db, EngineConfig())
    await engine.run()


if __name__ == '__main__':
    run(main())
