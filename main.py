import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.types import BotCommand
from dotenv import load_dotenv

from app.handlers import router
from app.admin import admin
from app.logger import logger
from database.models import create_db

# Включаем логирование, чтобы не пропустить важные сообщения
logger()


async def register_commands(bot):
    commands = [
        BotCommand(command='/start', description='Запуск бота'),
        BotCommand(command='/help', description='Помощь'),
        BotCommand(command='/status', description='Админка'),
        # Добавьте сюда свои команды
    ]
    await bot.set_my_commands(commands)


async def main():
    load_dotenv()

    session = AiohttpSession(
        api=TelegramAPIServer.from_base(os.getenv('LOCAL_BOT_API'))
    )

    # Объект бота
    bot = Bot(
        token=os.getenv('BOT_TOKEN'),
        default=DefaultBotProperties(parse_mode='HTML'),
        session=session
    )

    # Диспетчер
    dp = Dispatcher()

    # Создание таблиц
    await create_db()

    dp.include_routers(admin, router)

    # Регистрация команд
    await register_commands(bot)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
