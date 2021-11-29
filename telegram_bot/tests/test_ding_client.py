import asyncio

from telegram_bot.intergration import ding_bot_client
from telegram_bot.service.dingtalk import DingBotMessageService


def test_ding_bot():
    token = "e39e7de07156ecf40ff2411cd1b59a5fdfde7b6f7dd0b2469196dbf36db66f10"
    asyncio.run(DingBotMessageService.send_text(ding_bot_client, token, "天气预报123"))
