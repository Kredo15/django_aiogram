import aiohttp
from .local_settings import API_URL_NEW_WORD, API_URL_CATEGORIES


async def get_new_word(user_id: int,
                       name_category: str,
                       pk: int
                       ):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'{API_URL_NEW_WORD}/?user={user_id}&name_category={name_category}&pk={pk}'
        ) as response:
            return await response.json()


async def get_categories():
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'{API_URL_CATEGORIES}'
        ) as response:
            return await response.json()
