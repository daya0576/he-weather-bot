import os
from datetime import datetime
import pytz
import telegram


def weather_forecast(event, context):
    chat_ids = os.environ["CHAT_IDS"].split(',')
    tz = pytz.timezone('Asia/Shanghai')
    cur_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
    for chat_id in chat_ids:
        bot.send_message(chat_id=chat_id, text=f"测试 - 定时任务触发的天气预报({cur_time})：")
        bot.send_photo(chat_id=chat_id, photo="http://wttr.in/上海浦东_0pq.png?2FnM&lang=zh-cn")


if __name__ == '__main__':
    weather_forecast(None, None)
