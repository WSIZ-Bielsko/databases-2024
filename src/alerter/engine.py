import asyncio
from asyncio import run

from loguru import logger
from pydantic import BaseModel

from src.alerter.db_repository import EntityRepository, connect_db


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
            logger.info(f'sleeping for {next_action/3600} hours')
            await asyncio.sleep(self.config.check_schedule_hours * 3600)

    async def schedule_alerts(self):
        logger.info('Checking schedule for new alerts to create')
        # get all active schedules
        # for each such schedule
        #   check if get_last_alert for this schedule returns
        #       None, or last is already closed --> create new alert for this schedule
        #       else: do noting


    async def notify_on_alerts(self):
        logger.info('Acting on alerts')
        # pull all alerts
        # if they are close to alert_date:
        #   if severity <= 5 --> write a "warning" log to console
        #   else --> send alert message to discord (for now implement as if this were to console with extra WARNING in message



async def main():
    logger.info('Starting alerter engine')
    pool = await connect_db()
    db = EntityRepository(pool=pool)
    engine = AlerterEngine(db, EngineConfig())
    await engine.run()


if __name__ == '__main__':
    run(main())
