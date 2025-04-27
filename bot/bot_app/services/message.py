import asyncio
from aiogram.fsm.context import FSMContext
from bot.bot_app.services.exercise import get_word_for_learning
from bot.bot_app.keyboards import get_button_new_word, get_button_start_study
from bot.bot_app.app import bot


async def bot_send_message_new_word(state: FSMContext,
                                    user_id: int,
                                    name_category: str,
                                    pk_old: int = 0
                                    ) -> None:
    pk_new, en_word, ru_word = await get_word_for_learning(user_id=user_id,
                                                           name_category=name_category,
                                                           pk_old=pk_old)
    message = await bot.send_message(chat_id=user_id,
                                     text=f'{en_word}<span class="tg-spoiler"> - {ru_word}</span>',
                                     parse_mode='html',
                                     reply_markup=get_button_new_word())
    await state.update_data(pk=pk_new,
                            message_id=message.message_id,
                            new_word=dict(en_word=en_word, ru_word=ru_word,
                                          translate_choose_en=False,
                                          translate_choose_ru=False))


def get_final_message_for_study(data: dict) -> str:
    result = ""
    for value in data.values():
        result += f"{value['en_word']} - {value['ru_word']}\n"
    return f"Отлично! Готов изучить слова 📚?\n\n{result}"


async def send_final_message_for_study(state: FSMContext,
                                       user_id: int,
                                       data_study: dict):
    data = await state.get_data()
    message = await bot.send_message(chat_id=user_id,
                                     text=get_final_message_for_study(data_study),
                                     reply_markup=get_button_start_study())
    data["message_id"] = message.message_id
    await state.update_data(data)


async def delete_message(chat_id, curr_message, previous_message):
    await bot.delete_message(chat_id=chat_id, message_id=curr_message)
    await asyncio.sleep(0)
    await bot.delete_message(chat_id=chat_id, message_id=previous_message)