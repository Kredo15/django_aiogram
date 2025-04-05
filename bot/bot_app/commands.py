from .app import dp
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineQuery,\
    ChosenInlineResult
from aiogram import F
from aiogram.fsm.context import FSMContext
from .app import bot
from .keyboards import get_menu_inline, get_button_start_study
from .state import WordsStudy
from .services import get_inline_with_categories, bot_send_message_new_word, \
    add_word_in_dict_state, get_final_message_for_study


@dp.message(Command(commands=["help"]))
async def help_command(message: Message):
    await message.answer('Hello!\nI help you remember new words!')


@dp.message(Command(commands=["start", "menu"]))
async def start_command(message: Message):
    # проверить профиль пользователя
    await message.answer('Выбери действие', reply_markup=get_menu_inline())


@dp.inline_query(F.query == "categories")
async def show_category(inline_query: InlineQuery):
    results = await get_inline_with_categories()
    await inline_query.answer(results, is_personal=True)


@dp.chosen_inline_result()
async def start_study(chosen_result: ChosenInlineResult, state: FSMContext):
    await bot.send_message(chat_id=chosen_result.from_user.id, text="Great! let's start")
    await state.set_state(WordsStudy.new_word)
    data = await state.get_data()
    data['name_category'] = chosen_result.result_id
    await state.update_data(data)
    await bot_send_message_new_word(state=state,
                                    user_id=chosen_result.from_user.id,
                                    name_category=chosen_result.result_id)


@dp.message(WordsStudy.new_word, F.text == "Изучать")
async def study_word(message: Message, state: FSMContext):
    data = await state.get_data()
    data_update = add_word_in_dict_state(data=data)
    await state.update_data(data_update)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if len(data_update.get('study')) == 5:
        await message.answer(get_final_message_for_study(data_update.get('study')),
                             reply_markup=get_button_start_study())
    else:
        await bot_send_message_new_word(state=state,
                                        user_id=message.from_user.id,
                                        name_category=data['name_category'])


@dp.callback_query(F.data == "new_word")
async def choose_category(
        callback: CallbackQuery, state: FSMContext
):
    # await bot.send_message(chat_id=callback.message.chat.id, text='afeq', reply_markup=get_switch_button())
    await state.set_state(WordsStudy.new_word)
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)


@dp.callback_query(F.data == "popular_word")
async def send_message_beginning_study(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(f"Great! let's start")
    data = await state.get_data()
    data["category"] = callback.message.text
    await state.update_data(data)
    # res = await get_new_word(callback.message.from_user.id, 'популярные слова')
    # en_word = res.get('en_word').get('word')
    # ru_word = res.get('ru_word').get('word')
    # await callback.message.answer(f"{en_word} - {ru_word}", reply_markup=get_button_keyboard())
    # await state.set_state(WordsStudy.new_word)
