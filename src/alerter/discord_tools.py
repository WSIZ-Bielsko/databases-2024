import os
from discord import SyncWebhook
from dotenv import load_dotenv
from loguru import logger


def send_msg(hook: str, msg: str):
    # hook ~ https://discord.com/api/webhooks/102291033111111111/Y6Rlh9d_ZMw75TKBiAoAKI3tcuiDZzgDrtNQwiBt6Jg...
    webhook = SyncWebhook.from_url(hook)
    webhook.send(msg)


def send_critical_msg(hook: str, critical_group_id: str, msg: str):
    # sending messages to users in certain groups
    webhook = SyncWebhook.from_url(hook)
    # # webhook.send('<@&1022914607129575424> gg')
    webhook.send(f'<@&{critical_group_id}>\n' + msg)


def basic_usage():
    load_dotenv()
    discord_webhook = os.getenv('DISCORD_WEBHOOK', None)
    critical_group_id = os.getenv('CRITICAL_GROUP_ID', None)
    logger.info(f'using hook:{discord_webhook} and critical group {critical_group_id}')

    print(discord_webhook)
    # send_msg(discord_webhook, 'ok, works')


if __name__ == '__main__':
    basic_usage()
