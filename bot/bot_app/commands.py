from .app import dp
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup,\
                            CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F


def get_menu_inline():
    buttons = [
        [InlineKeyboardButton(text="Изучать новые слова", callback_data="new_word")],
        [InlineKeyboardButton(text="Выученные наполовину", callback_data="word_repetition")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

@dp.message(Command(commands=["help"]))
async def help_command(message: Message):
    await message.answer('Hello!\nI help you remember new words!')


@dp.message(Command(commands=["start", "menu"]))
async def start_command(message: Message):
    #добавить профиль пользователя 
    await message.answer('', reply_markup=get_menu_inline())


@dp.callback_query(F.data == "new_word")
async def send_random_value(callback: CallbackQuery):
    pass
