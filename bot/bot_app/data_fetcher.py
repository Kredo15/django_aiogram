import aiohttp
from .local_settings import API_URL_NEW_WORD, API_URL_CATEGORIES


async def get_new_word(user_id: int = None, name_category: str = None):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'{API_URL_NEW_WORD}/?user={user_id}&name_category={name_category}'
        ) as response:
            return await response.json()


async def get_categories():
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'{API_URL_CATEGORIES}'
        ) as response:
            return await response.json()
