from loguru import logger

from telegram_bot.database import crud
from telegram_bot.database.database import get_db_session
from telegram_bot.telegram.biz.weather import biz_send_warning, biz_send_weather


async def send_weather_by_user(user_id: str, user_cur_hour: str):
    logger.info(f"[send_weather_by_user]start,{user_id},{user_cur_hour}")
    with get_db_session() as db:
        chat = crud.get_user(db, user_id)
    if not chat or not chat.is_active:
        return {"message": "USER_NOT_FOUND"}

    return await biz_send_weather(chat, user_cur_hour)


async def send_warning_by_user(user_id: str):
    logger.info(f"[send_warning_by_user]start,{user_id}")
    with get_db_session() as db:
        chat = crud.get_user(db, user_id)
    if not chat or not chat.is_active:
        return {"message": "USER_NOT_FOUND"}

    return await biz_send_warning(chat)
