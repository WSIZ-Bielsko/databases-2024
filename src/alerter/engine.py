import asyncio
import os
from asyncio import run
from datetime import datetime
from uuid import uuid4, UUID

from asyncpg.pgproto.pgproto import timedelta
from dateutil.utils import today
from loguru import logger
from pydantic import BaseModel
from pydantic.v1 import UUID1

from src.alerter.db_repository import EntityRepository, connect_db
from src.alerter.discord_tools import DiscordNotifier
from src.alerter.model import Alert, Schedule

from croniter import croniter
from datetime import datetime


class EngineConfig(BaseModel):
    check_schedule_hours: int = 1
    repeat_alert_hours: int = 12


class AlerterEngine:

    def __init__(self, db: EntityRepository, config: EngineConfig, discord_notifier: DiscordNotifier = None):
        self.discord_notifier = discord_notifier
        self.config = config
        self.db = db
        self.last_alert_time = None

    async def run(self):
        logger.info('starting alerter engine')

        while True:
            await self.schedule_alerts()
            await self.notify_on_alerts()
            next_action = self.config.check_schedule_hours * 3600
            logger.info(f'sleeping for {next_action / 3600} hours')
            await asyncio.sleep(self.config.check_schedule_hours * 3600)

    def get_next_cron_timestamp(cron_expression, start_time=None):
        if start_time is None:
            start_time = datetime.now()
            cron = croniter(cron_expression, start_time)
            next_timestamp = cron.get_next(datetime)
            return next_timestamp

    async def schedule_alerts(self):
        """
        Ensure (next) alert objects are present for all active schedules
        """
        logger.info('checking schedule for new alerts to create')

        schedules = await self.db.list_active_schedules()

        for s in schedules:
            last_alert = await self.db.get_last_alert(s.id)
            if last_alert is None:
                due = None
                if s.period_days is not None:
                    due = today() + timedelta(days=s.period_days)
                elif s.cron_expression is not None:
                    due = self.get_next_cron_timestamp(s.cron_expression)

                if due is not None:
                    new_alert = Alert(
                        id=uuid4(),
                        schedule_id=s.id,
                        message=f"alert: {s.name}, due: {due.date()}",
                        alert_date=due,
                        closed_at=None,
                        close_message=None,
                    )
                    logger.info("creating new alert " + str(new_alert))
                    await self.db.create_alert(new_alert)

    async def notify_on_alerts(self):
        """
        Execute actions for all alert objects which are not far from alert_date
        """
        if (self.last_alert_time is None or
                datetime.now() - self.last_alert_time > self.config.repeat_alert_hours * 3600):

            self.last_alert_time = today()
            logger.info('acting on alerts')
            alerts = await self.db.list_nonclosed_alerts()
            for a in alerts:
                schedule = await self.db.get_schedule(a.schedule_id)

                days_before_due = (a.alert_date - today().date()).days
                logger.debug(f'checking alert {a}')
                logger.debug(f'{a.id}: {days_before_due} vs {schedule.critical_warning_days_before}')

                if (a.alert_date - today().date()).days > schedule.critical_warning_days_before:
                    continue

                logger.info('acting on {a}')
                if self.discord_notifier is not None and schedule.severity >= 5:
                    if schedule.severity >= 8 and self.discord_notifier.role_id is not None:
                        self.discord_notifier.send_critical_msg(a.message)
                    else:
                        self.discord_notifier.send_msg(a.message)
                else:
                    logger.warning('ALERT DUE:' + a.message)

    async def close_alert(self, alert_id: UUID, close_message: str):
        alert = await self.db.get_alert(alert_id)
        alert.closed_at = today()
        alert.close_message = close_message
        await self.db.update_alert(alert)

    async def create_schedule(self, schedule: Schedule):
        logger.info(f'creating new schedule {schedule}')
        await self.db.create_schedule(schedule)

    async def deactivate_schedule(self, schedule_id: UUID):
        schedule = await self.db.get_schedule(schedule_id)
        logger.info(f'deactivating schedule {schedule}')
        schedule.active = False
        await self.db.update_schedule(schedule)
