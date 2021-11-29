import functools

import sentry_sdk
from loguru import logger

from telegram_bot.intergration import DingBotClient
from telegram_bot.intergration.exceptions import DingBotException


def service_template(f):
    @functools.wraps(f)
    async def inner(bot: DingBotClient, token: str, msg: str):
        try:
            await f(bot, token, msg)
        except DingBotException as e:
            logger.error(e)
            sentry_sdk.capture_exception(e, "钉钉发送异常")
        except Exception as e:
            logger.error(e)
            sentry_sdk.capture_exception(e)
        else:
            logger.info(f"message send to {token}, msg: {msg}")

    return inner


class DingBotMessageService:
    """钉钉自定义机器人发送消息，包含异常处理"""

    @staticmethod
    @service_template
    async def send_text(bot: DingBotClient, token: str, msg: str):
        await bot.send_text(token, msg)
