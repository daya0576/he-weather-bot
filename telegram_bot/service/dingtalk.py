import functools

import sentry_sdk
from loguru import logger

from telegram_bot.intergration import ding_bot_client
from telegram_bot.intergration.exceptions import DingBotException


def service_template(f):
    @functools.wraps(f)
    async def inner(token: str, msg: str):
        try:
            await f(token, msg)
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
    async def send_text(token: str, msg: str):
        if not token or not msg:
            raise ValueError(f"参数非法,token:{token},msg:{msg}")
        await ding_bot_client.send_text(token, msg)
