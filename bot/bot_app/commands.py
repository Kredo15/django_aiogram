from .app import dp
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineQuery, \
    InlineQueryResultArticle, InputTextMessageContent, ChosenInlineResult
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from aiogram.fsm.context import FSMContext
from .app import bot
from .data_fetcher import get_new_word, get_categories
from .keyboards import get_menu_inline, get_button_keyboard
from .state import WordsStudy
from .services import start_learning, get_inline_with_categories
import uuid


@dp.message(Command(commands=["help"]))
async def help_command(message: Message):
    await message.answer('Hello!\nI help you remember new words!')


@dp.message(Command(commands=["start", "menu"]))
async def start_command(message: Message):
    #проверить профиль пользователя
    await message.answer('Выберите действие', reply_markup=get_menu_inline())


@dp.callback_query(F.data == "new_word")
async def choose_category(
        callback: CallbackQuery, state: FSMContext
):
    #await bot.send_message(chat_id=callback.message.chat.id, text='afeq', reply_markup=get_switch_button())
    await state.set_state(WordsStudy.new_word)
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)


@dp.inline_query(F.query == "categories")
async def show_category(inline_query: InlineQuery):
    results = await get_inline_with_categories()
    await inline_query.answer(results, is_personal=True)
    #await start_learning(user_id=inline_query.from_user.id, name_category=value['name'])


@dp.chosen_inline_result()
async def pagination_demo(chosen_result: ChosenInlineResult):
    await bot.send_message(chat_id=chosen_result.from_user.id, text="Great! let's start")
    print(chosen_result.json)
    word_for_study = await start_learning(user_id=chosen_result.from_user.id, name_category=chosen_result.result_id)
    await bot.send_message(word_for_study, reply_markup=get_button_keyboard())


@dp.callback_query(F.data == "popular_word")
async def send_message_beginning_study(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(f"Great! let's start")
    data = await state.get_data()
    data["category"] = callback.message.text
    print(data)
    await state.update_data(data)
    # res = await get_new_word(callback.message.from_user.id, 'популярные слова')
    # en_word = res.get('en_word').get('word')
    # ru_word = res.get('ru_word').get('word')
    # await callback.message.answer(f"{en_word} - {ru_word}", reply_markup=get_button_keyboard())
    # await state.set_state(WordsStudy.new_word)



