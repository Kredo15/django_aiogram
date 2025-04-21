from .app import dp
from aiogram.filters import Command
from aiogram.types import Message, InlineQuery, ChosenInlineResult, CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext
from .app import bot
from .keyboards import get_button_start_study, get_inline_menu

from .state import WordsStudy
from .services import get_inline_with_categories, bot_send_message_new_word, \
    get_data_after_study, get_data_after_skipping, get_final_message_for_study, \
    add_studied_word_in_user_dict, get_actions_depending_user
from .button_signature import STUDY, STOP_STUDY, KNOW


@dp.message(Command(commands=["help"]))
async def help_command(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Hello!\nI help you remember new words!',
                             reply_markup=get_inline_menu())
    else:
        await message.answer('Мы не закончили упражнение ☝️')


@dp.message(Command(commands=["start", "menu"]))
async def start_command(message: Message, state: FSMContext):
    user_actions = get_actions_depending_user(message.from_user.id)
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Выбери действие', reply_markup=user_actions())
    else:
        await message.answer('Мы не закончили упражнение ☝️')


@dp.callback_query(F.data == "menu")
async def choose_category(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=callback.message.message_id)
    await bot.send_message(chat_id=callback.message.chat.id, text='Выбери действие',
                           reply_markup=get_inline_actions())


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


@dp.message(WordsStudy.new_word, F.text == STUDY)
async def word_study(message: Message, state: FSMContext):
    data = await state.get_data()
    data_update = get_data_after_study(data=data)
    await state.update_data(data_update)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=data.get('message_id'))
    if len(data_update.get('study')) == 5:
        await message.answer(get_final_message_for_study(data_update.get('study')),
                             reply_markup=get_button_start_study())
    else:
        await bot_send_message_new_word(state=state,
                                        user_id=message.from_user.id,
                                        name_category=data['name_category'],
                                        pk_old=data['pk'])


@dp.message(WordsStudy.new_word, F.text == KNOW)
async def know_word(message: Message, state: FSMContext):
    data = await state.get_data()
    await add_studied_word_in_user_dict(user_id=message.from_user.id, data=data)
    data_update = get_data_after_skipping(data=data)


@dp.message(F.text == STOP_STUDY)
async def stop_study(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Мы не начинали упражнение 🤷‍')
    else:
        await state.clear()
        await message.answer('Ок, приходи за новыми знаниями! 🎓')
