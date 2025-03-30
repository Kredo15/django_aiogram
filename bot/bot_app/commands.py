from .app import dp
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from aiogram.fsm.context import FSMContext

from .data_fetcher import get_new_word
from .keyboards import get_menu_inline, get_button_keyboard
from .state import WordsStudy


@dp.message(Command(commands=["help"]))
async def help_command(message: Message):
    await message.answer('Hello!\nI help you remember new words!')


@dp.message(Command(commands=["start", "menu"]))
async def start_command(message: Message):
    #проверить профиль пользователя
    await message.answer('Выберите действие', reply_markup=get_menu_inline())


@dp.callback_query(F.data == "new_word")
async def send_word_study(callback: CallbackQuery, state: FSMContext):
    res = await get_new_word(callback.message.from_user.id, 'популярные слова')
    en_word = res[0].get('en_word').get('word')
    ru_word = res[0].get('ru_word').get('word')
    await callback.message.answer(f"{en_word} - {ru_word}", reply_markup=get_button_keyboard())
    await state.set_state(WordsStudy.new_word)

