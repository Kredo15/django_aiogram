from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from .keyboards import get_menu_inline
from .app import bot
from .keyboards import get_button_keyboard
from .data_fetcher import get_new_word, get_categories


async def get_inline_with_categories():
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


async def start_learning(user_id: int, name_category: str):
    res = await get_new_word(user_id, name_category)
    en_word = res[0].get('en_word').get('word')
    ru_word = res[0].get('ru_word').get('word')
    return f"{en_word} - {ru_word}"
    #await state.set_state(WordsStudy.new_word)
