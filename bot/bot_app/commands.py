import asyncio
from .app import dp
from aiogram.filters import Command
from aiogram.types import Message, InlineQuery, ChosenInlineResult, CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext
from .app import bot
from .keyboards import get_inline_menu
from .state import WordsStudy
from bot.bot_app.services.inline_button import get_inline_with_categories
from bot.bot_app.services.message import bot_send_message_new_word, \
    send_final_message_for_study, delete_message
from bot.bot_app.services.user import add_studied_word_in_user_dict, \
    get_actions_depending_user
from bot.bot_app.services.exercise import get_data_after_study, \
    get_data_after_skipping, send_studied_word
from .button_signature import STUDY, STOP_STUDY, KNOW, START


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
    user_actions = await get_actions_depending_user(message.from_user.id, message.from_user.username)
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Выбери действие', reply_markup=user_actions())
    else:
        await message.answer('Мы не закончили упражнение ☝️')


@dp.callback_query(F.data == "menu")
async def choose_category(callback: CallbackQuery, state: FSMContext):
    user_actions = await get_actions_depending_user(callback.from_user.id, callback.from_user.username)
    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=callback.message.message_id)
    await callback.message.answer(text='Выбери действие',
                                  reply_markup=user_actions())


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
    await delete_message(chat_id=message.chat.id, curr_message=message.message_id,
                         previous_message=data.get('message_id'))
    if len(data_update.get('study')) == 5:
        await send_final_message_for_study(state=state,
                                           user_id=message.from_user.id,
                                           data_study=data_update.get('study'))
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
    await state.update_data(data_update)
    await bot_send_message_new_word(state=state,
                                    user_id=message.from_user.id,
                                    name_category=data['name_category'],
                                    pk_old=data['pk'])


@dp.message(F.text == STOP_STUDY)
async def stop_study(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Мы не начинали упражнение 🤷‍')
    else:
        await state.clear()
        await message.answer('Ок, приходи за новыми знаниями! 🎓')


@dp.message(WordsStudy.new_word, F.text == START)
async def start_exercise(message: Message, state: FSMContext):
    data = await state.get_data()
    data['exercise'] = {'translate_choose_en': [str(i) for i in range(5)],
                        'translate_choose_ru': [str(i) for i in range(5)]}
    await state.update_data(data)
    await delete_message(chat_id=message.chat.id, curr_message=message.message_id,
                         previous_message=data.get('message_id'))
    await send_studied_word(state=state, message=message, data=data)


@dp.message(WordsStudy.new_word, F.text)
async def check_word_with_exercise(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == data.get("current_studied_word").get('true_word'):
        await message.answer(text='👌 right')
        key = data.get("current_studied_word").get('key')
        func = data.get("current_studied_word").get('func')
        data['study'][key][func] = True
        await state.update_data(data)
        await delete_message(chat_id=message.chat.id, curr_message=message.message_id,
                             previous_message=data.get('message_id'))
    else:
        await message.answer(text='❌ wrong')
    await send_studied_word(state=state, message=message, data=data)
