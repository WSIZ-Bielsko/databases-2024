import os
from discord import SyncWebhook
from dotenv import load_dotenv
from loguru import logger
from concurrent.futures import ThreadPoolExecutor


def send_msg(hook: str, msg: str):
    # hook ~ https://discord.com/api/webhooks/102291033111111111/Y6Rlh9d_ZMw75TKBiAoAKI3tcuiDZzgDrtNQwiBt6Jg...
    webhook = SyncWebhook.from_url(hook)
    webhook.send(msg)


def send_critical_msg(hook: str, role_id: str, msg: str):
    # sending messages to users in certain groups
    webhook = SyncWebhook.from_url(hook)
    # # webhook.send('<@&1022914607129575424> gg')
    webhook.send(f'<@&{role_id}>\n' + msg)


def basic_usage():
    load_dotenv()
    discord_webhook = os.getenv('DISCORD_WEBHOOK', None)
    role_id = os.getenv('ROLE_ID', '')
    logger.info(f'using hook:{discord_webhook} and critical group {role_id}')

    print(discord_webhook)
    # send_msg(discord_webhook, 'ok, works')
    send_critical_msg(discord_webhook, role_id, 'ok, critical works')


class DiscordNotifier:
    def __init__(self, webhook: str, role_id: str):
        self.webhook = webhook
        self.role_id = role_id
        self.executor = ThreadPoolExecutor(max_workers=4)

    def send_msg(self, msg: str):
        self.executor.submit(self._send_msg, self.webhook, msg)

    def send_critical_msg(self, msg: str):
        self.executor.submit(self._send_critical_msg, self.webhook, self.role_id, msg)

    def _send_msg(self, hook: str, msg: str):
        webhook = SyncWebhook.from_url(hook)
        webhook.send(msg)

    def _send_critical_msg(self, hook: str, role_id: str, msg: str):
        webhook = SyncWebhook.from_url(hook)
        webhook.send(f'<@&{role_id}>\n' + msg)


if __name__ == '__main__':
    basic_usage()
