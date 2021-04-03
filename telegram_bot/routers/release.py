import asyncio

from fastapi import Depends
from loguru import logger
from sentry_sdk import capture_exception
from sqlalchemy.orm import Session

from telegram_bot.database import crud, models
from telegram_bot.database.database import get_db
from telegram_bot.routers.cron import router
from telegram_bot.settings import aio_lru_cache_partial
from telegram_bot.telegram.components.keyboard_markup_factory import KeyboardMarkUpFactory
from telegram_bot.telegram.dispatcher import dp
from telegram_bot.telegram.service.message import TelegramMessageService

ONE_YEAR = 60 * 60 * 24 * 365

V0_1_0 = """
v0.1.1 稳定正式版已发布。如有任何问题，请联系 @daya0576

**✨ FEATURES**
1. 支持自定义通知时间（所在地时区）
2. 支持开启/关闭订阅
3. 告警样式优化（新增 emoji）
4. 支持群订阅

**🌝 BUG FiX**
1. 修复重复投递的问题
2. 修复消息丢失的问题（使命必达）
"""


@aio_lru_cache_partial(ttl=ONE_YEAR)
async def do_release(chat: models.Chat):
    """发送版本更新"""
    markup = KeyboardMarkUpFactory.build_main_menu(chat)
    await TelegramMessageService.send_keyboard_markup(dp.bot, chat.chat_id, V0_1_0, markup, parse_mode="Markdown")

    return True


@router.get("/release_v1")
async def cron_handler(db: Session = Depends(get_db)):
    all_active_users = crud.get_active_users(db)

    # 并行处理，单个 exception 不中断其他任务
    results = await asyncio.gather(
        *[do_release(user) for user in all_active_users],
        return_exceptions=True
    )
    # 汇总异常处理
    success = 0
    for result in results:
        if not isinstance(result, Exception):
            success += 1
            continue
        logger.exception(result)
        capture_exception(result)

    return {"result": f"{success}/{len(results)}"}
