from aiogram.fsm.context import FSMContext
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from .app import bot
from .keyboards import get_button_new_word
from .data_fetcher import get_new_word, get_categories
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


async def bot_send_message_new_word(state: FSMContext,
                                    user_id: int = None,
                                    name_category: str = None,
                                    pk_old: int = 0
                                    ) -> None:
    pk_new, en_word, ru_word = await get_word_for_learning(user_id=user_id,
                                                           name_category=name_category,
                                                           pk_old=pk_old)
    await state.update_data(new_word=dict(pk=pk_new, en_word=en_word, ru_word=ru_word))
    await bot.send_message(chat_id=user_id,
                           text=f'{en_word}<span class="tg-spoiler"> - {ru_word}</span>',
                           parse_mode='html',
                           reply_markup=get_button_new_word())


def add_word_in_dict_state(data: dict) -> dict:
    if data.get('new_word'):
        try:
            update_data = {len(data.get('study')): copy.deepcopy(data['new_word'])}
            data['study'].update(update_data)
        except KeyError:
            update_data = {0: copy.deepcopy(data['new_word'])}
            data['study'] = update_data
        data['new_word'] = None
        return copy.deepcopy(data)


def get_final_message_for_study(data: dict) -> str:
    result = ""
    for value in data.values():
        result += f"{value['en_word']} - {value['ru_word']}\n"
    return f"Отлично! Готов изучить слова 📚?\n\n{result}"
