from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def index():
    return {"message": "Hello World"}


@router.get("/cron")
def cron_handler():
    # send_weather_forecast_to_channel(bot)
    return 'ok'
