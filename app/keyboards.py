from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def categories(formats: [], options, url):
    if formats:
        keyboard = InlineKeyboardBuilder()
        for text, format_id in zip(formats, options):
            keyboard.add(InlineKeyboardButton(text=text, callback_data=f'{format_id} {url}'))
        return keyboard.adjust(1).as_markup()
