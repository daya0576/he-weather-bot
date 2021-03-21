from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from telegram_bot.database import models

WELCOME_TEXT = """
基于「和风」的天气预报机器人。根据用户位置查询实时天气，并每天自动播报。

如有任何问题，请联系 @daya0576    
"""

ENABLE_SUB, DISABLE_SUB = "enable_sub", "disable_sub"
GET_WEATHER, UPDATE_LOCATION = "weather", "edit"
UPDATE_SUB_CRON = "update_cron"
EXIT = "back"

HOURS = tuple(x for x in range(0, 24, 2))


class KeyboardMarkUpFactory:
    @staticmethod
    def build_main_menu(chat: "models.Chat") -> InlineKeyboardMarkup:
        keyboard_markup = InlineKeyboardMarkup(row_width=6)

        # 第一行：天气获取
        weather_button = InlineKeyboardButton('获取实时天气', callback_data=GET_WEATHER)
        keyboard_markup.add(weather_button)

        # 第二行：自定义配置
        inline_buttons = [InlineKeyboardButton('更新位置', callback_data=UPDATE_LOCATION)]
        if chat:
            sub_cron_button = InlineKeyboardButton('通知时间', callback_data=UPDATE_SUB_CRON)
            inline_buttons.append(sub_cron_button)

        star_button = InlineKeyboardButton('关注项目✨', url="https://github.com/daya0576/he_weather_bot")
        inline_buttons.append(star_button)
        keyboard_markup.row(*inline_buttons)

        return keyboard_markup

    @staticmethod
    def build_cron_options() -> InlineKeyboardMarkup:
        keyboard_markup = InlineKeyboardMarkup(row_width=6)

        chunk_size = 6
        for x in range(0, len(HOURS), chunk_size):
            items = []
            for i in HOURS[x:x + chunk_size]:
                btn = InlineKeyboardButton(str(i), callback_data=str(i))
                items.append(btn)
            keyboard_markup.row(*items)

        keyboard_markup.add(InlineKeyboardButton("返回", callback_data=EXIT))
        return keyboard_markup
