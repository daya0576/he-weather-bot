from fastapi import APIRouter

from telegram_bot.database import crud
from telegram_bot.database.database import SessionLocal
from telegram_bot.intergration import he_weather
from telegram_bot.telegram.dispatcher import dp

router = APIRouter()


@router.get("/")
async def index():
    return {"message": "Hello World"}


@router.get("/cron")
async def cron_handler():
    users = crud.get_users(SessionLocal())

    for user in users:
        text = he_weather.get_weather_forecast(user.location)
        await dp.bot.send_message(chat_id=user.chat_id, text=text)

    return 'ok'
