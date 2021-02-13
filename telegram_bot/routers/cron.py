from fastapi import APIRouter

from telegram_bot.database import crud

router = APIRouter()


@router.get("/")
async def index():
    return {"message": "Hello World"}


@router.get("/cron")
def cron_handler():
    users = crud.get_users()
    # send_weather_forecast_to_channel(bot)
    return 'ok'
