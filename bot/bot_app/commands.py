from .app import dp
from aiogram.filters import Command
from aiogram.types import Message


@dp.message(Command(commands=["help"]))
async def help_command(message: Message):
    await message.answer('Hello!\nI help you remember new words!')
