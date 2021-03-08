from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from telegram_bot.database import models


class KeyboardMarkUpFactory:
    @staticmethod
    def build(user: "models.Chat") -> InlineKeyboardMarkup:
        keyboard_markup = InlineKeyboardMarkup(row_width=6)

        keyboard_markup.add(
            InlineKeyboardButton('获取实时天气', callback_data='weather'),
        )

        inline_buttons = [InlineKeyboardButton('更新位置', callback_data="edit")]
        if user:
            sub_button = InlineKeyboardButton(
                '关闭订阅' if user.is_active else '开启订阅',
                callback_data="disable" if user.is_active else "enable"
            )
            inline_buttons.append(sub_button)
        inline_buttons.append(InlineKeyboardButton('关注项目✨', url="https://github.com/daya0576/he_weather_bot"))
        keyboard_markup.row(*inline_buttons)

        return keyboard_markup
