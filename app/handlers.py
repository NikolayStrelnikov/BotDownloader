import re
from datetime import datetime

from aiogram import Bot, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

import database.requests as db
from app.workers import select_format, download_process

router = Router()

# Regular expression for validating YouTube URLs
# YOUTUBE_REGEX = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+')
URL_REGEX = re.compile(
    r'((http|https)://)?'  # Протокол (http или https)
    r'([a-zA-Z0-9.-]+)'  # Доменное имя
    r'(\.[a-zA-Z]{2,})'  # Домен верхнего уровня
    r'(/[a-zA-Z0-9._~:/?#@!$&\'()*+,;=%-]*)?'  # Путь и параметры
)


class UrlProtect(Filter):
    def __init__(self):
        self.url_reg = URL_REGEX

    async def __call__(self, message: Message):
        return self.url_reg.match(message.text)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await db.set_user(user_id=message.from_user.id,
                      nick=message.from_user.username,
                      name=message.from_user.first_name,
                      surname=message.from_user.last_name,
                      locale=message.from_user.language_code,
                      date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                      )

    content = f'Привет! Отправь мне ссылку на видео. Я скачаю его для тебя'
    await message.answer(content, parse_mode='HTML')

@router.message(Command('help'))
async def cmd_help(message: Message, bot: Bot):
    bot_info = await bot.get_me()
    bot_name = bot_info.first_name
    await message.reply(f'Тут будет описание возможностей бота <b>{bot_name}</b>')

@router.message(UrlProtect(), F.text)
async def download_start(message: Message):
    await select_format(message=message)


@router.callback_query(lambda c: True)
async def process_download(callback_query: CallbackQuery):
    format_id = callback_query.data.split(' ')[0]
    url = callback_query.data.split(' ')[1]
    # await callback.answer('Формат выбран')
    print(f'ФОРМАТ: {format_id} ССЫЛКА: {url}')
    await download_process(message=callback_query.message, format_id=format_id, url=url)





@router.message(F.text)
async def download_action(message: Message):
    await message.reply('Пожалуйста, отправьте ссылку на видео')
