import os
from asyncio import run

from dotenv import load_dotenv
from loguru import logger

from src.alerter.db_repository import connect_db, EntityRepository
from src.alerter.discord_tools import DiscordNotifier
from src.alerter.engine import AlerterEngine, EngineConfig


async def app():
    logger.info('Starting alerter app')
    load_dotenv()
    discord_webhook = os.getenv('DISCORD_WEBHOOK', None)
    role_id = os.getenv('ROLE_ID', None)
    if discord_webhook is None:
        logger.warning('no DISCORD_WEBHOOK provided, alerts will be logged to console instead of discord')
    else:
        if role_id is None:
            logger.warning('no ROLE_ID provided, critical alerts will just be posted to discord, '
                           'without @mentioning anyone')
    notifier = DiscordNotifier(discord_webhook, role_id) if discord_webhook else None
    pool = await connect_db()
    db = EntityRepository(pool=pool)
    engine = AlerterEngine(db, EngineConfig(), discord_notifier=notifier)
    await engine.run()


if __name__ == '__main__':
    run(app())
