from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from bot_app.data_fetcher import get_categories


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
