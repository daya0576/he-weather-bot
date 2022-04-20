import asyncio
import time

import pytest
from dotenv import load_dotenv

load_dotenv(".env_test")
from telegram_bot.database.models import Chat, DingBots
from telegram_bot.cron import tasks
from telegram_bot.intergration.weather.models.warn_model import WarnModel

fake_warn_model = WarnModel("text", "type", "level")
same_fake_warn_model = WarnModel("text", "type", "level")
diff_fake_warn_model = WarnModel("text_diff", "type", "level")
fake_chat = Chat()
fake_chat.latitude = 123
fake_chat.longitude = 123
fake_ding_bot = DingBots()


@pytest.fixture(scope="function")
def mockit(mocker):
    # mock weather api
    warning_mock = mocker.patch(
        'telegram_bot.intergration.weather.he_weather_client.HeWeatherClient.get_weather_warning')
    warning_mock.return_value = WarnModel("text", "type", "level")
    # mock telegram api
    message_mock = mocker.patch('telegram_bot.service.telegram.TelegramMessageService.send_text')
    mocker.patch('telegram_bot.service.dingtalk.DingBotMessageService.send_text')
    return warning_mock, message_mock


def test_diff_warnings(mockit):
    warning_mock, message_mock = mockit
    asyncio.run(tasks.cron_send_warning(fake_chat, fake_ding_bot))
    asyncio.run(tasks.cron_send_warning(fake_chat, fake_ding_bot))
    asyncio.run(tasks.cron_send_warning(fake_chat, fake_ding_bot))
    assert message_mock.call_count == 1

    # same warnings
    warning_mock.return_value = same_fake_warn_model
    asyncio.run(tasks.cron_send_warning(fake_chat, fake_ding_bot))
    assert message_mock.call_count == 1

    # different warnings
    warning_mock.return_value = diff_fake_warn_model
    asyncio.run(tasks.cron_send_warning(fake_chat, fake_ding_bot))
    assert message_mock.call_count == 2
    asyncio.run(tasks.cron_send_warning(fake_chat, fake_ding_bot))
    assert message_mock.call_count == 2

    # waiting for cache expire
    time.sleep(1)
