import aiohttp
from .local_settings import API_URL_NEW_WORD, API_URL_CATEGORIES, \
    API_URL_STUDIED_WORD, API_URL_USER, API_AUTH_USER, API_USERS_FOR_ACTIVITY


async def get_new_word(user_id: int,
                       name_category: str,
                       pk: int
                       ):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'{API_URL_NEW_WORD}?user={user_id}&name_category={name_category}&pk={pk}'
        ) as response:
            return await response.json()


async def get_categories():
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'{API_URL_CATEGORIES}'
        ) as response:
            return await response.json()


async def add_studied_word(data: list):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                url=f'{API_URL_STUDIED_WORD}',
                json=data
        ) as response:
            return await response.json()


async def get_auth_user(user: int):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                url=f'{API_AUTH_USER}',
                json={
                    "username": user,
                    "password": user
                }
        ) as response:
            return await response.json()


async def get_user_data(username: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=f'{API_URL_USER}?user={username}'
        ) as response:
            return await response.json()


async def add_user(user_id: int, username: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                url=f'{API_URL_USER}',
                json={"user": {
                                "username": user_id,
                                "first_name": username,
                                "password": user_id
                            }
                      }
        ) as response:
            return await response.json()


async def get_user_for_activity():
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=f'{API_USERS_FOR_ACTIVITY}'
        ) as response:
            return await response.json()
