from aiogram.fsm.context import FSMContext
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from .app import bot
from .keyboards import get_button_new_word
from .data_fetcher import get_new_word, get_categories, add_studied_word
import copy


async def get_inline_with_categories() -> list[InlineQueryResultArticle]:
    categories = await get_categories()
    results = []
    for value in categories:
        results.append(InlineQueryResultArticle(
            id=value['name'],
            title=value['name'],
            input_message_content=InputTextMessageContent(
                disable_web_page_preview=True,
                message_text=f"learning words from the category {value['name']}"
            )
        ))
    return results


async def get_word_for_learning(user_id: int,
                                name_category: str,
                                pk_old: int
                                ) -> tuple[int, str, str]:
    res = await get_new_word(user_id, name_category, pk_old)
    pk_new = res.get('id')
    en_word = res.get('en_word').get('word')
    ru_word = res.get('ru_word').get('word')
    return pk_new, en_word, ru_word


async def add_studied_word_in_user_dict(user_id: int, data: dict) -> None:
    data_for_send = {
        "user": user_id,
        "word": data['pk'],
        "translate_choose_ru": True,
        "translate_choose_en": True,
        "translate_write_ru": True,
        "translate_write_en": True,
        "write_word_using_audio": True,
        "is_learn": True
    }
    await add_studied_word(data_for_send)


async def bot_send_message_new_word(state: FSMContext,
                                    user_id: int = None,
                                    name_category: str = None,
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
                            new_word=dict(en_word=en_word, ru_word=ru_word))


def get_data_after_study(data: dict) -> dict:
    if data.get('new_word'):
        try:
            update_data = {len(data.get('study')): copy.deepcopy(data['new_word'])}
        except TypeError:
            update_data = {0: copy.deepcopy(data['new_word'])}
        try:
            data['study'].update(update_data)
        except KeyError:
            data['study'] = update_data
        data['new_word'] = None
        return data


def get_data_after_skipping(data: dict) -> dict:
    if data.get('new_word'):
        data['new_word'] = None
        return data


def get_final_message_for_study(data: dict) -> str:
    result = ""
    for value in data.values():
        result += f"{value['en_word']} - {value['ru_word']}\n"
    return f"Отлично! Готов изучить слова 📚?\n\n{result}"
