import os

from aiogram import Router
from aiogram.filters import Command, Filter
from aiogram.types import Message

admin = Router()

# Получите список администраторов из переменной окружения
admins_str = os.getenv('ADMINS')
ADMINS = list(map(int, admins_str.split(','))) if admins_str else []


class AdminProtect(Filter):
    def __init__(self):
        self.admins = ADMINS

    async def __call__(self, message: Message):
        # print(f'PASS {message.from_user.id} {self.admins}')
        return message.from_user.id in self.admins


@admin.message(AdminProtect(), Command('status'))
async def ap(message: Message):
    await message.answer('Это панель администратора')
