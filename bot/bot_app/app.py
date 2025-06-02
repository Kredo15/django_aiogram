from aiogram import Bot, Dispatcher
import os
from aiogram.fsm.storage.redis import RedisStorage


API_KEY_BOT = os.getenv('API_KEY_BOT')
storage = RedisStorage.from_url(os.getenv('REDIS_URL').strip())
bot = Bot(token=API_KEY_BOT)
dp = Dispatcher(storage=storage)
