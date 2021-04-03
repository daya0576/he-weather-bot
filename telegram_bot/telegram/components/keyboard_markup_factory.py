from typing import Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from telegram_bot.database import models

WELCOME_TEXT = """
基于「和风」的天气预报机器人；根据定位查询精准实时天气，并每天自动播报。

如有任何问题，请联系 @daya0576    
"""

ENABLE_SUB, DISABLE_SUB = "enable_sub", "disable_sub"
GET_WEATHER, UPDATE_LOCATION = "weather", "edit"
UPDATE_SUB_CRON = "update_cron"
BACK = "back"

HOURS = tuple(str(x) for x in range(0, 24, 2))


class KeyboardMarkUpFactory:
    @staticmethod
    def build_main_menu(chat: "models.Chat") -> InlineKeyboardMarkup:
        keyboard_markup = InlineKeyboardMarkup(row_width=6)

        # 第一行：天气获取
        weather_button = InlineKeyboardButton('获取实时天气', callback_data=GET_WEATHER)
        keyboard_markup.add(weather_button)

        # 第二行：自定义配置
        inline_buttons = [InlineKeyboardButton('更新位置', callback_data=UPDATE_LOCATION)]
        if chat and chat.is_location_exist:
            sub_cron_button = InlineKeyboardButton('通知时间', callback_data=UPDATE_SUB_CRON)
            inline_buttons.append(sub_cron_button)

        star_button = InlineKeyboardButton('关注项目✨', url="https://github.com/daya0576/he_weather_bot")
        inline_buttons.append(star_button)
        keyboard_markup.row(*inline_buttons)

        return keyboard_markup

    @staticmethod
    def build_cron_options(chat: "models.Chat") -> Optional[InlineKeyboardMarkup]:
        if not chat:
            return

        keyboard_markup = InlineKeyboardMarkup(row_width=6)

        chunk_size = 6
        for x in range(0, len(HOURS), chunk_size):
            inline_btn_list = []
            for hour in HOURS[x:x + chunk_size]:
                hour_formatted = f"{hour}✓" if hour in chat.sub_hours else hour
                btn = InlineKeyboardButton(hour_formatted, callback_data=hour)
                inline_btn_list.append(btn)
            keyboard_markup.row(*inline_btn_list)

        back_btn = InlineKeyboardButton("返回", callback_data=BACK)
        keyboard_markup.add(back_btn)
        return keyboard_markup
