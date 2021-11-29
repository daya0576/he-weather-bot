from typing import Dict

from telegram_bot.intergration.exceptions import DingBotException
from telegram_bot.intergration.http.base_http_client import HttpClient

WEBHOOK_TEMPLATE = "https://oapi.dingtalk.com/robot/send?access_token={}"
ERRCODE_KEY = "errcode"


class DingBotClient:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    async def _do_execute(self, webhook: str, param: Dict):
        d = await self.http_client.post(webhook, param)
        if d.get(ERRCODE_KEY) != 0:
            # https://developers.dingtalk.com/document/app/server-api-error-codes-1
            raise DingBotException(f"dingding hook failed: {d}")

    async def send_text(self, token, msg):
        webhook = WEBHOOK_TEMPLATE.format(token)
        param = {"msgtype": "text", "text": {"content": msg}}
        await self._do_execute(webhook, param)
